"""
Tests for the hostname/nodelist utility module
"""
import slurmlint.hosts as hosts


def test_expand_numlist():
    expected = [
        '05', '06', '07', '009', '010', '011', '012', '013', '04', '4'
    ]
    assert hosts.expand_numlist('05-07,009-13,04,4') == expected
