#!/usr/bin/python3

import os
import jinja2
import tempfile
import subprocess

bases = ['debian']

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
        with open(base_dfpath, "w") as f:
            f.write(template.render(base=base))
        subprocess.run(['sudo', '/ecs/utils/container/bin/subuildah', 'bud', '-f', base_dfpath, context_dir], check=True)




