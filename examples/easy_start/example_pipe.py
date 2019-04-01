"""
Author: dohmatob elvis dopgima elvis[dot]dohmatob[at]inria[dot]fr
Synopsis: Minimal script for preprocessing single-subject data
"""

import os
import time
import numpy as np
import nibabel
from pypreprocess.nipype_preproc_spm_utils import do_subjects_preproc
from pypreprocess.datasets import fetch_spm_auditory
from pypreprocess.reporting.glm_reporter import generate_subject_stats_report
import pandas as pd
from pypreprocess.external.nistats.design_matrix import (make_design_matrix,
                                                         check_design_matrix,
                                                         plot_design_matrix)
from pypreprocess.external.nistats.glm import FirstLevelGLM
import matplotlib.pyplot as plt

# file containing configuration for preprocessing the data
this_dir = os.path.dirname(os.path.abspath(__file__))
jobfile = os.path.join(this_dir, "spm_auditory_preproc.ini")

# fetch spm auditory data
sd = fetch_spm_auditory()
dataset_dir = os.path.dirname(os.path.dirname(os.path.dirname(sd.anat)))

# construct experimental paradigm
stats_start_time = time.ctime()
tr = 7.
n_scans = 96
_duration = 6
n_conditions = 2
epoch_duration = _duration * tr
conditions = ['rest', 'active'] * 8
duration = epoch_duration * np.ones(len(conditions))
onset = np.linspace(0, (len(conditions) - 1) * epoch_duration,
                    len(conditions))
paradigm = pd.DataFrame(
    {'onset': onset, 'duration': duration, 'name': conditions})

hfcut = 2 * 2 * epoch_duration
fd = open(sd.func[0].split(".")[0] + "_onset.txt", "w")
for c, o, d in zip(conditions, onset, duration):
    fd.write("%s %s %s\r\n" % (c, o, d))
fd.close()

# preprocess the data
subject_data = do_subjects_preproc(jobfile, dataset_dir=dataset_dir)[0]
