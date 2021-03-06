#!/router/bin/python3.8.2_mcpre-v1 -u
# -----------------------------------------------------------------------------
# runtest.py -- Framework for running tests
#
# December 2020, Patrick Smears
#
# Copyright (c) 2020 by Cisco Systems, Inc.
# All rights reserved.
# -----------------------------------------------------------------------------

import os
import sys
import jinja2
import shutil
import filecmp
import tempfile
import argparse
import subprocess

script_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

buildah = ["sudo", "/ecs/utils/container/bin/subuildah"]
podman = ["sudo", "/ecs/utils/container/bin/supodman"]

imagename = "xrscripttest"

bases = {"debian": {"name": "Debian 9",
                    "from": "debian:9.13-slim"},
         "centos": {"name": "CentOS 7",
                    "from": "centos:7.0.1406"}}

files = [
    "xr-image-extract-rpms",
    "setup/prep-{base}",
]

test_files = [
    "test/test-xr-image-extract-rpms",
]    

isos = [
    "/release/IOX/bin/7.2.1/8000-x64-7.2.1.iso",
    "/release/IOX/bin/7.0.11/8000-x64-7.0.11.iso",
]

tenv = jinja2.Environment(loader=jinja2.FileSystemLoader(script_root))
dockerfile_template = tenv.get_template("test/template.dockerfile")
readme_template = tenv.get_template("test/template.README.md")

def create_dockerfile(fname, base, *, extra_files=[], isos=[], entrypoint="/bin/bash"):
    base_info = bases[base]
    with open(fname, "w") as f:
        f.write(
            dockerfile_template.render(
                base=base,
                from_=base_info["from"],
                files=[f.format(base=base) for f in (files + extra_files)],
                isos=[os.path.basename(i) for i in isos],
                entrypoint=entrypoint,
            )
        )

def create_readme(fname):
    for basename, base in bases.items():
        with open(os.path.join(script_root, "setup/prep-{}".format(basename)), "r") as f:
            base["prep"] = "".join("    "+line for line in f if not line.startswith("#-"))
    with open(fname, "w") as f:
        f.write(
            readme_template.render(
                bases=bases.values(),
            )
        )

def perform_tests():
    with tempfile.TemporaryDirectory() as tmpdir:
        dockerfile_dir = os.path.join(tmpdir, "dockerfiles")
        os.mkdir(dockerfile_dir)

        context_dir = os.path.join(tmpdir, "context")
        os.mkdir(context_dir)

        for base, base_info in bases.items():
            base_df = "{}.dockerfile".format(base)
            base_dfpath = os.path.join(dockerfile_dir, base_df)

            for f in files + test_files:
                f_base = f.format(base=base)
                src = os.path.join(script_root, f_base)
                dst = os.path.join(context_dir, f_base)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                shutil.copymode(src, dst)
            for i in isos:
                shutil.copyfile(i, os.path.join(context_dir, os.path.basename(i)))

            create_dockerfile(base_dfpath, base, extra_files=test_files, isos=isos, entrypoint="test-xr-image-extract-rpms")
            os.system("grep '' '{}'".format(base_dfpath))
            os.system("find '{}'".format(context_dir))
            cmd = buildah + ["bud", "-t", imagename, "-f", base_dfpath, context_dir]
            res = subprocess.run(cmd, capture_output=True)
            sys.stderr.buffer.write(res.stderr)
            if res.returncode != 0:
                print("Buildah command failed: {}", repr(cmd))
                sys.exit(1)
            else:
                imageid = res.stdout

            subprocess.run(podman + ["run", "--name", imagename, imagename])
            subprocess.run(podman + ["rm", imagename])
            subprocess.run(podman + ["rmi", imagename])

def compare_files(f1, f2, update):
    result = False
    if os.path.exists(f2) and filecmp.cmp(f1, f2):
        # Files compare equal - no action
        result = True
    else:
        if update:
            print("Updating '{}'".format(f2))
            shutil.copyfile(f1, f2)
            result = True
        else:
            if not os.path.exists(f2):
                print("File '{}' missing - rerun with --update to update".format(f2))
            else:
                print("Content of '{}' not as expected - rerun with --update to update".format(f2))
    return result
            
def generate_files(update):
    with tempfile.TemporaryDirectory() as tmpdir:
        dockerfile = os.path.join(tmpdir, "Dockerfile")
        create_dockerfile(dockerfile, "debian")
        readme = os.path.join(tmpdir, "README.md")
        create_readme(readme)
        all_ok = all([compare_files(dockerfile, "Dockerfile", update),
                      compare_files(readme, "README.md", update)])
                  
    if not all_ok:
        sys.exit(2)
    
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update generated docs / configuration files")
    parser.add_argument("--verify", action="store_true", help="Verify generated docs / configuration files")
    parser.add_argument("--test", action="store_true", help="Run container-based tests")

    args = parser.parse_args()

    # If nothing specified, go with some defaults:
    if not (args.test or args.update or args.verify):
        args.verify = True
        args.test = True

    if args.test:
        perform_tests()

    if args.update or args.verify:
        generate_files(args.update)

