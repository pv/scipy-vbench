#!/usr/bin/env python
"""make.py [COMMANDS]

Python script for building documentation.

To build the docs you must have all optional dependencies for statsmodels
installed. See the installation instructions for a list of these.

Note: currently latex builds do not work because of table formats that are not
supported in the latex generation.

"""

import os
import shutil
import argparse
import sys
import subprocess

sys.path.insert(0, 'vbench')

SPHINX_BUILD = 'sphinxbuild'

def run():
    subprocess.check_call([sys.executable, 'run_suite.py'])


def run_full():
    subprocess.check_call([sys.executable, 'run_suite.py', '--full'])


def upload():
    'push a copy to the site'
    """
    # Generated gh-pages are bulky, so why to carry them around?
    # We still probably like to use them for 'free hosting' but regenerating upon every build from scratch and
    # then gc and repacking archive
    git branch -D gh-pages
    git gc --aggressive
    ghp-import -p build/html -n
    git push -f origin gh-pages
    """
    print "D: removing previous gh-pages branches locally and from the origin"
    os.system('git branch -D gh-pages ; git branch -rd origin/gh-pages; git gc --aggressive --prune=now ; ghp-import -p build/html -n; git push -f origin gh-pages')

def clean():
    if os.path.exists('build'):
        shutil.rmtree('build')

def generate_rsts():
    """Prepare build/source which acquires original RST_BASE with generated files placed in
    """
    from vbench.reports import generate_rst_files, generate_rst_analysis
    from suite import benchmarks, DB_PATH, RST_BASE, DESCRIPTION, REPO_BROWSE, BRANCHES


    os.system('rsync -a %s build/' % RST_BASE)
    outpath = os.path.join('build', RST_BASE)
    generate_rst_analysis(
                   benchmarks,
                   dbpath=DB_PATH,
                   outpath=outpath,
                   gh_repo=REPO_BROWSE)
    generate_rst_files(benchmarks,
                   dbpath=DB_PATH,
                   outpath=outpath,
                   branches=BRANCHES,
                   description=DESCRIPTION + """

.. include:: analysis.rst

""")
    return outpath

def html():
    check_build()
    outpath = generate_rsts()
    if os.system('sphinx-build -P -b html -d build/doctrees '
                 '%s build/html' % outpath):
        raise SystemExit("Building HTML failed.")
    if os.system('touch build/html/.nojekyll'):
        raise SystemExit("Touching nojekyll file managed to fail.")

def latex():
    check_build()
    if sys.platform != 'win32':
        # LaTeX format.
        if os.system('sphinx-build -b latex -d build/doctrees '
                     'source build/latex'):
            raise SystemExit("Building LaTeX failed.")
        # Produce pdf.

        os.chdir('build/latex')

        # Call the makefile produced by sphinx...
        if os.system('make'):
            raise SystemExit("Rendering LaTeX failed.")

        os.chdir('../..')
    else:
        print 'latex build has not been tested on windows'

def check_build():
    build_dirs = [
        'build', 'build/doctrees', 'build/html',
        'build/latex', 'build/plots', 'build/_static',
        'build/_templates']
    for d in build_dirs:
        try:
            os.mkdir(d)
        except OSError:
            pass

def all():
    clean()
    html()
    #upload()

funcd = {
    'update'   : update,
    'html'     : html,
    'latex'    : latex,
    'clean'    : clean,
    'upload'   : upload,
    'all'      : all,
    }

small_docs = False

def main():
    p = argparse.ArgumentParser(usage=__doc__.lstrip())
    p.add_argument('commands', nargs='+',
                   help=", ".join(sorted(funcd.keys())))
    args = p.parse_args()

    for arg in args.commands:
        if arg not in funcd:
            p.error('Do not know how to handle %s; valid args are %s' % (
                arg, funcd.keys()))

    for arg in args.commands:
        funcd[arg]()

    sys.exit(0)

if __name__ == "__main__":
    main()
