#!/usr/bin/env python
"""
run_suite.py [OPTIONS]
"""
import sys
import os
import logging
import argparse

os.environ['PATH'] = os.pathsep.join(
    ['/usr/lib/ccache', '/usr/local/lib/f90cache']
    + os.environ.get('PATH').split(os.pathsep)
    )
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'vbench')))

from vbench.api import BenchmarkRunner, verify_benchmarks
from vbench.config import is_interactive

import suite

log = logging.getLogger('vb')


def run_process(existing='min', run_order='multires', run_limit=None, run_option='all'):
    runner = BenchmarkRunner(suite.benchmarks,
                             suite.REPO_PATH,
                             suite.REPO_URL,
                             suite.BUILD,
                             suite.DB_PATH,
                             suite.TMP_DIR,
                             suite.PREPARE,
                             branches=suite.BRANCHES,
                             clean_cmd=suite.PREPARE,
                             run_option=run_option, 
                             run_order=run_order,
                             run_limit=run_limit,
                             start_date=suite.START_DATE,
                             existing=existing,
                             module_dependencies=suite.dependencies,
                             verify=True)
    runner.run()


def main():
    p = argparse.ArgumentParser(usage=__doc__.lstrip())
    p.add_argument('--verify', action='store_true')
    args = p.parse_args()

    if args.verify:
        verify_benchmarks(suite.benchmarks, raise_=True)
    else:
        try:
            # quick pass through to get at least some results for only
            # new benchmarks and/or commits
            run_process(existing='skip', run_order='multires', run_option='eod')
            # now a thorough pass through trying to get better
            # estimates for some of previous without running all of them
            #run_process(existing='min', run_order='random', run_limit=100)
        except Exception as exc:
            log.error('%s (%s)' % (str(exc), exc.__class__.__name__))
            if __debug__ and is_interactive(): # and args.common_debug:
                import pdb
                pdb.post_mortem()
            raise


if __name__ == '__main__':
    main()
