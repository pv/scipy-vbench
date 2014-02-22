#/bin/sh
PATH=/usr/lib/ccache:/usr/local/lib/f90cache:$PATH PYTHONPATH=$PWD/vbench ./run_suite.py "$@"
