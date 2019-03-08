"""
The cli entry point for linting slurm configs
"""
import argparse
import sys

from slurmlint.linter import lint
from slurmlint.__version__ import __version__


def cli():
    """
    CLI entry point for Slurm Configuration Linter
    Run ``slurmlint --help`` for usage
    """
    version_msg = 'slurmlint, version {0}'.format(__version__)
    description = 'Slurm Configuration File Linter'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-v', '--version',
        action='version',
        help="Print the version of slurmlint",
        version=version_msg
    )
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    try:
        data = open(args.filename).read()
    except Exception:
        print('Error: could not read input file')
        sys.exit(1)

    result = lint(data)
    print('{0} compute nodes configured'.format(len(result['nodes'])))
    if not result['errors']:
        sys.exit(0)
    print('')
    print('Errors detected:')
    for error in result['errors']:
        print('Line {0} - {1}'.format(error[0], error[1]))
    sys.exit(1)
