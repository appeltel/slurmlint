![Travis CI Status](https://travis-ci.org/appeltel/slurmlint.svg?branch=master)
![python 3.5, 3.6, 3.7](https://img.shields.io/badge/python-3.5%2C%203.6%2C%203.7-brightgreen.svg)

# slurmlint

Simple linter for Slurm Config Files

## Hostname Lists

This linter applies stricter rules than Slurm for lists of hostnames.
Hostnames must be valid hostnames according to
[RFC-1123](https://tools.ietf.org/html/rfc1123), that is they may contain
a-z, 0-9, dot, and the minus sign, at most 253 ASCII characters, and must
be comprised of "labels" from 1-63 characters connected by dots.

Hostnames can be separated by commas in a list.

The standard (???) rules for brackets apply. If a list entry uses brackets
to denote some numerical range or comma separated list, there must be
brackets at the end of the hostname. One can also have a bracketed range
somewhere else in the hostname provided that there are brackets at the end.
Brackets may contain valid non-negative integers separated by commas, or
ranges such as `1-8`. A leading zero in a range denotes a fixed width, i.e.
`001-020`.

Note that this linter does not use the slurm parser and will result in
"false positive" warnings where allowed hostname ranges still result in
warnings.
