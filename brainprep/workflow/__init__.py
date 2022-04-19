# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2022
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module that implements all user workflows.
"""

# Imports
from .fsreconall import brainprep_fsreconall, brainprep_fsreconallqc
from .cat12vbm import brainprep_cat12vbm, brainprep_cat12vbmqc
from .quasiraw import brainprep_quasiraw, brainprep_quasirawqc
from .fmriprep import brainprep_fmriprep
from .mriqc import brainprep_mriqc
