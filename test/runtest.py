#!/usr/bin/python3

import os
import jinja2
import tempfile
import subprocess

buildah = ['sudo', '/ecs/utils/container/bin/subuildah']

bases = ['debian']

files = ['xr-image-extract-rpms', 'test/test-xr-image-extract-rpms']

tenv = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
template = tenv.get_template("template.dockerfile")

with tempfile.TemporaryDirectory() as tmpdir:
    dockerfile_dir = os.path.join(tmpdir, "dockerfiles")
    os.mkdir(dockerfile_dir)

    context_dir = os.path.join(tmpdir, "context")
    os.mkdir(context_dir)


    for base in bases:
        base_df = '{}.dockerfile'.format(base)
        base_dfpath = os.path.join(dockerfile_dir, base_df)

        for f in files:
            os.link(os.path.join('..', f), 
                    os.path.join(context_dir, os.path.basename(f)))

        with open(base_dfpath, "w") as f:
            f.write(template.render(base=base))
        cmd = buildah + ['bud', '-t', 'xrscripttest', '-f', base_dfpath, context_dir]
        res = subprocess.run(cmd, capture_output=True)
        sys.stderr.buffer.write(res.stderr)
        if res.returncode != 0:
            print("Buildah command failed: {}", repr(cmd))
            sys.exit(1)
        else:
            imageid = res.stdout




