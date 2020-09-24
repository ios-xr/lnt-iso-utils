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


    for base in bases:
        base_df = '{}.dockerfile'.format(base)
        base_dfpath = os.path.join(tmpdir, base_df)
        with open(base_dfpath, "w") as f:
            f.write(template.render(base=base))
        subprocess.run(['sudo', '/ecs/utils/container/bin/supodman', 'build', '-f', base_dfpath], check=True)




