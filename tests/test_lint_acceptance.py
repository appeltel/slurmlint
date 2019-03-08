"""
Acceptance tests for the linter against real slurm.conf files

confing files should be placed in the assets directory and be named in the
form "slurm.conf.X.E-Y" if the first error is on the Yth line, or
"slurm.conf.X.OK" if there are no errors.
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

    eline_expected = int(conf.split('-')[1])
    assert result['errors'][1][0] == eline_expected
