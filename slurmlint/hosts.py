"""
Utility functions for expanding out and verifying lists of hostnames
"""
import re


RE_ISNUM = re.compile('[0-9]+')
RE_NEXTBRACKET = re.compile('([^[]*)\[([^]]*)\](.*)')


def expand_hostlist(hostlist, max_depth=20):
    """
    Given a slurm-style list of hosts, expand and
    return individual hostnames.

    :param str hostlist: slurm-style host list
    :param int max_depth: maximum number of brackets in an entry
    :returns: list of hostnames
    :rtype: list(str)
    """
    result = _split_outside_brackets(hostlist, ',')
    depth = 0
    while depth < max_depth:
        if not any(host.endswith(']') for host in result):
            return result
        depth += 1

        new_result = []
        for item in result:
            if not item.endswith(']'):
                new_result.append(item)
            else:
                new_result.extend(_expand_next_bracket(item))

        result = new_result

    raise ValueError('Too many brackets') 


def _split_outside_brackets(raw, splitchar):
    """
    Split a string on a given character only when the
    character is outside brackets

    Nested brackets are right out
    """
    result = []
    word = ''
    in_brackets = False
    for char in raw:
        if char == '[' and not in_brackets:
            word = word + char
            in_brackets = True
        elif char == '[' and in_brackets:
            raise ValueError('Nested brackets are right out')
        elif char == ']' and in_brackets:
            word = word + char
            in_brackets = False
        elif char == ']' and not in_brackets:
            raise ValueError('Unmatched end-bracket')
        elif not in_brackets and char == splitchar and word:
            result.append(word)
            word = ''
        elif not in_brackets and char == splitchar and not word:
            raise ValueError('Missing item between separator')
        else:
            word = word + char
    if not word:
        raise ValueError('Missing item after separator')
        
    result.append(word)
    return result


def _expand_next_bracket(hostlist):
    """
    Take a hostlist and expand the next set of brackets
    returning a list of either hosts or hostlists if
    there are multiple brackets.
    """
    if not hostlist.endswith(']'):
        raise ValueError(
            'Invalid host list, not ending in bracket'
        )
    match = RE_NEXTBRACKET.match(hostlist)
    if not match:
        raise ValueError('Invalid brackets in host list')
    prefix = match.group(1)
    numlist = match.group(2)
    suffix = match.group(3)
    return [prefix + num + suffix for num in expand_numlist(numlist)] 


def expand_numlist(raw):
    """
    Expand a comma-delimited list of numbers and/or numeric ranges

    :param str raw: String containing list of numbers to be expanded
    :returns: List of expanded numbers
    :rtype: list(str)
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
