![Travis CI Status](https://travis-ci.org/appeltel/slurmlint.svg?branch=master)
![python 3.5, 3.6, 3.7](https://img.shields.io/badge/python-3.5%2C%203.6%2C%203.7-brightgreen.svg)

# A Simple linter for Slurm Config Files

## Purpose

In my experience it is very easy to make small errors in slurm configuration
files, incorrectly listing nodes in the cluster, or failing to assign nodes
to partitions, and so on. This package provides a simple command to check
slurm files that is suitable for use in automated deployment management.

In addition, a python API is provided allowing checking arbitrary strings
of text. Utility functions such as explanding slurm-style hostname lists
are also given.

## Usage

The `slurmlint` command takes a slurm configuration file as an argument
and returns a simple report with errors (if any). If there were errors
then the return code is 1, otherwise 0.

```
$ slurmlint slurm.conf
753 compute nodes configured

Errors detected:
Line 126 - Duplicate node definition: ng1031, ng908, ng909, ...
Line 127 - Duplicate node definition: ng1031
Line 128 - Duplicate node definition: ng908, ng909, ng910
Line 131 - Defined node has no partition: ng1259
Line 131 - Duplicate node definition: ng1256
```

## Limitations

This utility does not fully understand the grammar of slurm configuration
files and does not guarantee the validity of a configuration file. It only
serves to help find certain kinds of simple errors. 

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
