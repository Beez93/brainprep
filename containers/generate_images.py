#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2022
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import glob
import fire
import shutil


def main(working_dir):
    """ Parse available Docker files and generates associated images.

    Parameters
    ----------
    working_dir: str
        the directory where the images will be generated.
    """
    image_dir = os.path.dirname(os.path.abspath(__file__))
    for path in glob.glob(os.path.join(image_dir, "Dockerfile.*")):
        basename = os.path.basename(path)
        name = basename.split(".", 1)[1]
        if name in ("dmriprep", ):
            continue
        dest_dir = os.path.join(working_dir, name)
        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)
        tmp_dir = os.path.join(dest_dir, "tmp")
        cache_dir = os.path.join(dest_dir, "cache")
        for _path in (tmp_dir, cache_dir):
            if not os.path.isdir(_path):
                os.mkdir(_path)
        shutil.copy(path, os.path.join(dest_dir, "Dockerfile"))
        cmds = "export WDIR={}\n".format(dest_dir)
        cmds += "cd $WDIR\n"
        cmds += "export IMG={}\n".format(name)
        cmds += "sudo docker build --tag brainprep-$IMG .\n"
        cmds += "sudo docker images\n"
        cmds += ("sudo docker save -o brainprep-$IMG-latest.tar "
                 "brainprep-$IMG:latest\n")
        cmds += "sudo chmod 755 brainprep-$IMG-latest.tar\n"
        cmds += ("sudo SINGULARITY_TMPDIR=$WDIR/tmp SINGULARITY_CACHEDIR="
                 "$WDIR/cache singularity build brainprep-$IMG-latest.simg "
                 "docker-archive://brainprep-$IMG-latest.tar\n")
        cmds += "singularity inspect brainprep-$IMG-latest.simg\n"
        cmds_file = os.path.join(dest_dir, "commands")
        with open(cmds_file, "wt") as of:
            of.write(cmds)
        print("Ready to execute: {}".format(cmds_file))

    for path in glob.glob(os.path.join(image_dir, "Singularity.*")):
        basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        name = basename.split(".", 1)[1]
        docker_path = os.path.join(dirname, "Dockerfile.{}".format(name))
        if not os.path.isfile(docker_path):
            raise ValueError("Please define the '{}' docker file associated "
                             "to the singularity recipe.".format(docker_path))
        dest_dir = os.path.join(working_dir, name)
        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)
        home_dir = os.path.join(dest_dir, "home")
        tmp_dir = os.path.join(dest_dir, "tmp")
        cache_dir = os.path.join(dest_dir, "cache")
        for _path in (tmp_dir, cache_dir, home_dir):
            if not os.path.isdir(_path):
                os.mkdir(_path)
        shutil.copy(path, os.path.join(dest_dir, "Singularity"))
        shutil.copy(docker_path, os.path.join(dest_dir, "Dockerfile"))
        cmds = "export WDIR={}\n".format(dest_dir)
        cmds += "cd $WDIR\n"
        cmds += "export IMG={}\n".format(name)
        cmds += "mkdir $WDIR/home\n"
        cmds += "mkdir $WDIR/tmp\n"
        cmds += "mkdir $WDIR/cache\n"
        cmds += ("sudo SINGULARITY_TMPDIR=$WDIR/tmp "
                 "SINGULARITY_CACHEDIR=$WDIR/cache "
                 "SINGULARITY_HOME=$WDIR/home "
                 "singularity build brainprep-$IMG-latest.simg Singularity\n")
        cmds += "singularity sif list brainprep-$IMG-latest.simg\n"
        cmds += ("singularity sif dump 4 brainprep-$IMG-latest.simg "
                 "> data.squash\n")
        cmds += "unsquashfs -dest data data.squash\n"
        cmds += "docker build --tag brainprep-$IMG .\n"
        cmds += "sudo docker images\n"
        cmds += ("sudo docker save -o brainprep-$IMG-latest.tar "
                 "brainprep-$IMG:latest\n")
        cmds += "sudo chmod 755 brainprep-$IMG-latest.tar\n"
        cmds_file = os.path.join(dest_dir, "commands")
        with open(cmds_file, "wt") as of:
            of.write(cmds)
        print("Ready to execute: {}".format(cmds_file))


if __name__ == "__main__":

    fire.Fire(main)
