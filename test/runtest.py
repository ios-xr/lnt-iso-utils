#!/router/bin/python3.8.2_mcpre-v1

import os
import sys
import jinja2
import shutil
import tempfile
import subprocess

buildah = ['sudo', '/ecs/utils/container/bin/subuildah']
podman = ['sudo', '/ecs/utils/container/bin/supodman']

imagename = 'xrscripttest'

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
            shutil.copyfile(os.path.join('..', f), 
                            os.path.join(context_dir, os.path.basename(f)))

        with open(base_dfpath, "w") as f:
            f.write(template.render(base=base, files=[os.path.basename(f) for f in files]))
            os.system("grep '' '{}'".format(base_dfpath))
        cmd = buildah + ['bud', '-t', imagename, '-f', base_dfpath, context_dir]
        res = subprocess.run(cmd, capture_output=True)
        sys.stderr.buffer.write(res.stderr)
        if res.returncode != 0:
            print("Buildah command failed: {}", repr(cmd))
            sys.exit(1)
        else:
            imageid = res.stdout

        cmd = podman + ['run', imagename]
        subprocess.run(cmd)




