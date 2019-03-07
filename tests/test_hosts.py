"""
Tests for the hostname/nodelist utility module
"""
import slurmlint.hosts as hosts


def test_expand_numlist():
    expected = [
        '05', '06', '07', '009', '010', '011', '012', '013', '04', '4'
    ]
    assert hosts.expand_numlist('05-07,009-13,04,4') == expected

    expected = ['5', '123', '5017', '5018', '5019']
    assert hosts.expand_numlist('5,123,5017-5019') == expected


def test_expand_hostlist():
    expected = [
        'ng032', 'cn304', 'cn305', 'cn306', 'cn308', 'gpu0012', 'gpu0013',
        'gpu0014', 'gpu0015', 'gpu0022', 'gpu0023', 'gpu0024', 'gpu0025'
    ]
    result = hosts.expand_hostlist('ng032,cn[304-306,308],gpu00[1-2][2-5]')
    assert result == expected
