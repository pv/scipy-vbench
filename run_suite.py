#!/usr/bin/env python
"""
run_suite.py [OPTIONS]
"""
import sys
import os
import logging
import argparse
import subprocess

os.environ['PATH'] = os.pathsep.join(
    ['/usr/lib/ccache', '/usr/local/lib/f90cache']
    + os.environ.get('PATH', '').split(os.pathsep)
    )
vbench_pth = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vbench'))
benchmark_pth = os.path.abspath(os.path.join(os.path.dirname(__file__), 'benchmarks'))
sys.path.insert(0, vbench_pth)
sys.path.insert(0, benchmark_pth)
os.environ['PYTHONPATH'] = os.pathsep.join(
    [vbench_pth] + os.environ.get('PYTHONPATH', '').split(os.pathsep)
    )


from vbench.api import BenchmarkRunner, verify_benchmarks
from vbench.config import is_interactive

import suite

log = logging.getLogger('vb')


def clone_repo():
    git_dir = os.path.join(suite.REPO_PATH, '.git')
    if not os.path.isdir(git_dir):
        subprocess.check_call(['git', 'clone', '-o', 'origin', suite.REPO_URL, suite.REPO_PATH])

    cwd = os.getcwd()
    try:
        os.chdir(suite.REPO_PATH)
        subprocess.check_call(['git', 'fetch', 'origin'])
        subprocess.check_call(['git', 'clean', '-dxf'])
        subprocess.check_call(['git', 'reset', '--hard'])
        subprocess.check_call(['git', 'checkout', 'master'])
        for branch in suite.BRANCHES:
            if branch != 'master':
                subprocess.check_call(['git', 'branch', '-f', branch, 'origin/' + branch])
        subprocess.check_call(['git', 'reset', '--hard', 'origin/master'])
    finally:
        os.chdir(cwd)


def run_process(existing='min', run_order='multires', run_limit=None, run_option='all'):
    clone_repo()
    runner = BenchmarkRunner(suite.benchmarks,
                             suite.REPO_PATH,
                             suite.REPO_PATH,
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
    p.add_argument('--full', action='store_true')
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
            if args.full:
                run_process(existing='min', run_order='random', run_limit=100)
        except Exception as exc:
            log.error('%s (%s)' % (str(exc), exc.__class__.__name__))
            if __debug__ and is_interactive(): # and args.common_debug:
                import pdb
                pdb.post_mortem()
            raise


if __name__ == '__main__':
    main()
