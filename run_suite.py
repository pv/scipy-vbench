#!/usr/bin/env python
import logging, os, sys

try:
    import scipy
except ImportError:
    # yoh: In a clean chroot I use I disabled system-wide numpy altogether
    # as a paranoid measure to assure that benchmark scripts do not use it
    # anyhow.  Since they would not inherit this sys.path, I am pointing
    # to local numpy build, since it is needed for proper
    # collection/processing of benchmarks
    sys.path.insert(1, os.path.join(os.getcwd(), "scipy"))

from vbench.api import BenchmarkRunner, verify_benchmarks
from vbench.config import is_interactive

from suite import *

log = logging.getLogger('vb')

def run_process(existing='min', run_order='multires', run_limit=None):
    runner = BenchmarkRunner(benchmarks, REPO_PATH, REPO_URL,
                             BUILD, DB_PATH, TMP_DIR, PREPARE,
                             branches=BRANCHES,
                             clean_cmd=PREPARE,
                             run_option='all', run_order=run_order, run_limit=run_limit,
                             start_date=START_DATE,
                             existing=existing,
                             module_dependencies=dependencies,
                             verify=True)
    runner.run()

if __name__ == '__main__':
    import sys
    if 'verify' in sys.argv:
        verify_benchmarks(benchmarks, raise_=True)
    else:
        try:
            # quick pass through to get at least some results for only
            # new benchmarks and/or commits
            run_process(existing='skip', run_order='multires')
            # now a thorough pass through trying to get better
            # estimates for some of previous without running all of them
            run_process(existing='min', run_order='random', run_limit=100)
        except Exception as exc:
            log.error('%s (%s)' % (str(exc), exc.__class__.__name__))
            if __debug__ and is_interactive(): # and args.common_debug:
                import pdb
                pdb.post_mortem()
            raise

