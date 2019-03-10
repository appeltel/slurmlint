"""
Acceptance tests for the linter against real slurm.conf files

confing files should be placed in the assets directory and be named in the
form "slurm.conf.X.E-DESC" if there are errors, or
"slurm.conf.X.OK" if there are no errors. "DESC" should be a one-word
description of the error.

If there are errors, the first line of the slurm conf should
be a comment that ends with a comma delimited list of lines with errors.
"""
import os

import pytest

import slurmlint.linter as linter

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(THIS_DIR, 'assets')
CONF_FILES = [
    (c, open(os.path.join(ASSET_DIR, c)).read())
    for c in os.listdir(ASSET_DIR)
    if c.startswith('slurm.conf')
]

@pytest.mark.parametrize('conf,data', CONF_FILES)
def test_lint_conf_file(conf, data):
    result = linter.lint(data)
    if conf.endswith('OK'):
        assert result['errors'] == []
        return

    errors_in = data.splitlines()[0].split()[-1]
    eline_expected = [int(item) for item in errors_in.split(',')]
    eline_result = [item[0] for item in result['errors']]
    assert  eline_result == eline_expected
