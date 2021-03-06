from datetime import datetime
import logging
import os

from vbench.api import collect_benchmarks

log = logging.getLogger('vb')
log.setLevel(logging.INFO)

benchmarks = collect_benchmarks(['vb_sparse'])

log.info("Initializing settings")

cur_dir = os.path.dirname(__file__)
REPO_URL = 'https://github.com/scipy/scipy.git'
REPO_BROWSE = 'https://github.com/scipy/scipy'
DB_PATH = os.path.join(cur_dir, 'db/benchmarks.db')
REPO_MIRROR = os.path.join(cur_dir, 'scipy')
REPO_PATH = os.path.join(cur_dir, 'tmp', 'scipy')
TMP_DIR = os.path.join(cur_dir, 'tmp', 'tmp')

# Assure corresponding directories existence
for s in (REPO_PATH, os.path.dirname(DB_PATH), TMP_DIR):
    if not os.path.exists(s):
        os.makedirs(s)

BRANCHES = ['master']

# : python setup.py clea
PREPARE = """
git clean -dfx
"""

BUILD = """
python setup.py build_ext --inplace
"""

DESCRIPTION = """
These historical benchmark graphs were produced with `vbench
<http://github.com/pydata/vbench>`__ (ATM with yet to be integrated
upstream changes in https://github.com/pydata/vbench/pull/33).

Original repository with the The `scipy_vb_common
<https://github.com/pv/scipy-vbench/blob/master/scipy_vb_common.py>`__
setup script defining various variables and data structures used
through-out the bench can be found on github_ .

This suite is based on Yaroslav Halchenko's numpy-vbench_ rig.

.. _github: https://github.com/pv/scipy-vbench

.. _numpy-vbench: https://github.com/yarikoptic/numpy-vbench

"""
dependencies = ['scipy_vb_common.py']

# for now -- arbitrary day in the memorable past when scipy existed
# already
START_DATE = datetime(2013, 03, 01)
#START_DATE = datetime(2012, 06, 20)

# Might not even be there and I do not see it used
# repo = GitRepo(REPO_PATH)

RST_BASE = 'source'
