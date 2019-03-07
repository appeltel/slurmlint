"""
Utility functions for expanding out and verifying lists of hostnames
"""
import re


RE_ISNUM = re.compile('[0-9]+')


def _expand_numlist(raw):
    """
    Expand a comma-delimited list of numbers and/or numeric ranges
    """
    result = []
    for item in raw.split(','):
        if not '-' in item:
            if not RE_ISNUM.match(item):
                raise ValueError('Invalid numeric value')
            result.append(item)
            continue

        vals = item.split('-')
        if not len(vals) == 2:
            raise ValueError('Invalid numeric range')
        result.extend(_expand_numrange(vals[0], vals[1]))
    return result


def _expand_numrange(first, last):
    """
    Expand a range of numbers that may be zero-prefixed into a list
    """
    if not RE_ISNUM.match(first) or not RE_ISNUM.match(last):
        raise ValueError('Invalid numeric value')
    if int(last) < int(first):
        raise ValueError('Invalid range')

    fixed = first.startswith('0')
    if fixed:
        return [
            str(val).zfill(len(first))
            for val in range(int(first), int(last) + 1)
        ]

    return [str(val) for val in range(int(first), int(last) + 1)]
