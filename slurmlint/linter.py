"""
This is the linter
"""
from io import StringIO

from slurmlint.hosts import expand_hostlist


def lint(conf):
    """
    Lint the Slurm configuration file text and return
    a dict with a list of errors and other information.

    :param str conf: Slurm configuration file text
    :returns: dict containing list of errors in the configuration
    :rtype: dict
    """
    results = {'errors': [], 'nodes': []}

    for idx, line in enumerate(conf.splitlines()):
        if line.startswith('NodeName'):
            try:
                nodes = _parse_nodename_line(line)
                results['nodes'].extend(nodes)
            except Exception:
                results['errors'].append(
                    (idx+1, 'Invalid NodeName directive')
            )
            if len(results['nodes']) != len(set(results['nodes'])):
                results['errors'].append(
                    (idx, 'Duplicate nodes defined')
                )

    return results


def _parse_nodename_line(line):
    """
    Parse a nodename line and return a list of hosts
    """
    args = line.split()
    nodelist = args[0].split('=')[1]
    return expand_hostlist(nodelist)
