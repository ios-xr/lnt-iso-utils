#!/router/bin/python3.8.2_mcpre-v1 -u

import os
import sys
import jinja2
import shutil
import tempfile
import subprocess

buildah = ["sudo", "/ecs/utils/container/bin/subuildah"]
podman = ["sudo", "/ecs/utils/container/bin/supodman"]

imagename = "xrscripttest"

bases = {"debian": {"from": "debian:9.13-slim"}, "centos": {"from": "centos:7.0.1406"}}

files = [
    "xr-image-extract-rpms",
    "test/prep-{base}",
    "packages-{base}",
    "test/test-xr-image-extract-rpms",
]

isos = [
    "/release/IOX/bin/7.2.1/8000-x64-7.2.1.iso",
    "/release/IOX/bin/7.0.11/8000-x64-7.0.11.iso",
]

tenv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
template = tenv.get_template("template.dockerfile")


def create_dockerfile(fname, base):
    with open(fname, "w") as f:
        f.write(
            template.render(
                base=base,
                from_=base_info["from"],
                files=[os.path.basename(f.format(base=base)) for f in files],
                isos=[os.path.basename(i) for i in isos],
            )
        )


with tempfile.TemporaryDirectory() as tmpdir:
    dockerfile_dir = os.path.join(tmpdir, "dockerfiles")
    os.mkdir(dockerfile_dir)

    context_dir = os.path.join(tmpdir, "context")
    os.mkdir(context_dir)

    for base, base_info in bases.items():
        base_df = "{}.dockerfile".format(base)
        base_dfpath = os.path.join(dockerfile_dir, base_df)

        for f in files:
            f_base = f.format(base=base)
            shutil.copyfile(
                os.path.join("..", f_base),
                os.path.join(context_dir, os.path.basename(f_base)),
            )
            shutil.copymode(
                os.path.join("..", f_base),
                os.path.join(context_dir, os.path.basename(f_base)),
            )
        for i in isos:
            shutil.copyfile(i, os.path.join(context_dir, os.path.basename(i)))

        create_dockerfile(base_dfpath, base)
        os.system("grep '' '{}'".format(base_dfpath))
        cmd = buildah + ["bud", "-t", imagename, "-f", base_dfpath, context_dir]
        res = subprocess.run(cmd, capture_output=True)
        sys.stderr.buffer.write(res.stderr)
        if res.returncode != 0:
            print("Buildah command failed: {}", repr(cmd))
            sys.exit(1)
        else:
            imageid = res.stdout

        cmd = podman + ["run", imagename]
        subprocess.run(cmd)
