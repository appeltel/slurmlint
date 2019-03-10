"""
This is the linter
"""
from collections import Counter, defaultdict

from slurmlint.hosts import expand_hostlist


ALLOWED_PARAMS = [
    "include",
    "accountingstoragebackuphost",
    "accountingstorageenforce",
    "accountingstoragehost",
    "accountingstorageloc",
    "accountingstoragepass",
    "accountingstorageport",
    "accountingstoragetres",
    "accountingstoragetype",
    "accountingstorageuser",
    "accountingstorejobcomment",
    "acctgathernodefreq",
    "acctgatherenergytype",
    "acctgatherinfinibandtype",
    "acctgatherfilesystemtype",
    "acctgatherprofiletype",
    "allowspecresourcesusage",
    "authinfo",
    "authtype",
    "backupaddr",
    "backupcontroller",
    "batchstarttimeout",
    "burstbuffertype",
    "checkpointtype",
    "clustername",
    "communicationparameters",
    "completewait",
    "controladdr",
    "controlmachine",
    "corespecplugin",
    "cpufreqdef",
    "cpufreqgovernors",
    "cryptotype",
    "debugflags",
    "defmempercpu",
    "defmempernode",
    "defaultstoragehost",
    "defaultstorageloc",
    "defaultstoragepass",
    "defaultstorageport",
    "defaultstoragetype",
    "defaultstorageuser",
    "disablerootjobs",
    "eiotimeout",
    "enforcepartlimits",
    "epilog",
    "epilogmsgtime",
    "epilogslurmctld",
    "extsensorsfreq",
    "extsensorstype",
    "fairsharedampeningfactor",
    "fastschedule",
    "federationparameters",
    "firstjobid",
    "getenvtimeout",
    "grestypes",
    "groupupdateforce",
    "groupupdatetime",
    "healthcheckinterval",
    "healthchecknodestate",
    "healthcheckprogram",
    "inactivelimit",
    "jobacctgathertype",
    "jobacctgatherfrequency",
    "jobacctgatherparams",
    "jobcheckpointdir",
    "jobcomphost",
    "jobcomploc",
    "jobcomppass",
    "jobcompport",
    "jobcomptype",
    "jobcompuser",
    "jobcontainertype",
    "jobcredentialprivatekey",
    "jobcredentialpubliccertificate",
    "jobfileappend",
    "jobrequeue",
    "jobsubmitplugins",
    "keepalivetime",
    "killonbadexit",
    "killwait",
    "nodefeaturesplugins",
    "launchparameters",
    "launchtype",
    "licenses",
    "logtimeformat",
    "maildomain",
    "mailprog",
    "maxarraysize",
    "maxjobcount",
    "maxjobid",
    "maxmempercpu",
    "maxmempernode",
    "maxstepcount",
    "maxtaskspernode",
    "mcsparameters",
    "mcsplugin",
    "memlimitenforce",
    "messagetimeout",
    "minjobage",
    "mpidefault",
    "mpiparams",
    "msgaggregationparams",
    "overtimelimit",
    "plugindir",
    "plugstackconfig",
    "powerparameters",
    "powerplugin",
    "preemptmode",
    "preempttype",
    "prioritydecayhalflife",
    "prioritycalcperiod",
    "priorityfavorsmall",
    "priorityflags",
    "priorityparameters",
    "prioritymaxage",
    "priorityusageresetperiod",
    "prioritytype",
    "priorityweightage",
    "priorityweightfairshare",
    "priorityweightjobsize",
    "priorityweightpartition",
    "priorityweightqos",
    "priorityweighttres",
    "privatedata",
    "proctracktype",
    "prolog",
    "prologepilogtimeout",
    "prologflags",
    "prologslurmctld",
    "propagateprioprocess",
    "propagateresourcelimits",
    "propagateresourcelimitsexcept",
    "rebootprogram",
    "reconfigflags",
    "requeueexit",
    "requeueexithold",
    "resumefailprogram",
    "resumeprogram",
    "resumerate",
    "resumetimeout",
    "resvepilog",
    "resvoverrun",
    "resvprolog",
    "returntoservice",
    "routeplugin",
    "sallocdefaultcommand",
    "sbcastparameters",
    "schedulerparameters",
    "schedulertimeslice",
    "schedulertype",
    "selecttype",
    "selecttypeparameters",
    "slurmuser",
    "slurmdparameters",
    "slurmduser",
    "slurmctldaddr",
    "slurmctlddebug",
    "slurmctldhost",
    "slurmctldlogfile",
    "slurmctldparameters",
    "slurmctldpidfile",
    "slurmctldplugstack",
    "slurmctldport",
    "slurmctldprimaryoffprog",
    "slurmctldprimaryonprog",
    "slurmctldsyslogdebug",
    "slurmctldtimeout",
    "slurmddebug",
    "slurmdlogfile",
    "slurmdpidfile",
    "slurmdport",
    "slurmdspooldir",
    "slurmdsyslogdebug",
    "slurmdtimeout",
    "slurmschedlogfile",
    "slurmschedloglevel",
    "srunepilog",
    "srunportrange",
    "srunprolog",
    "statesavelocation",
    "suspendexcnodes",
    "suspendexcparts",
    "suspendprogram",
    "suspendrate",
    "suspendtime",
    "suspendtimeout",
    "switchtype",
    "taskepilog",
    "taskplugin",
    "taskpluginparam",
    "taskprolog",
    "tcptimeout",
    "tmpfs",
    "topologyparam",
    "topologyplugin",
    "trackwckey",
    "treewidth",
    "unkillablestepprogram",
    "unkillablesteptimeout",
    "usepam",
    "vsizefactor",
    "waittime",
    "x11parameters",
    "nodename",
    "partitionname"
]


def lint(conf):
    """
    Lint the Slurm configuration file text and return
    a dict with a list of errors and other information.

    :param str conf: Slurm configuration file text
    :returns: dict containing list of errors in the configuration
    :rtype: dict
    """
    linter = _SlurmLinter()
    return linter.lint(conf)


class _SlurmLinter:
    """
    Lints a slurm file text
    """
    def __init__(self):
        self.results = {'errors': []}
        self.nb = NodeBank()

        #set generic dispatch for parameters
        self.dispatch = {param: self._generic_line for param in ALLOWED_PARAMS}
        # special functions for important parameters
        self.dispatch['nodename'] = self._nodename_line
        self.dispatch['partitionname'] = self._partitionname_line

    def lint(self, conf):
        self.conf = conf
        for idx0, line in enumerate(conf.splitlines()):
            idx = idx0 + 1
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            param = line.split('=')[0].strip().lower()
            if param not in self.dispatch:
                self.results['errors'].append((idx, 'Invalid parameter'))
                continue
            self.dispatch[param](idx, line)

        self.results['errors'].extend(self.nb.duplicate_definition_errors())
        self.results['errors'].extend(self.nb.undefined_node_errors())
        self.results['errors'].extend(
            self.nb.node_missing_partition_errors()
        )
        self.results['errors'].sort()
        self.results['nodes'] = [node for node in self.nb]
        self.results['nodes'].sort()
        self.results['partitions'] = [part for part in self.nb.partitions]

        return self.results

    def _nodename_line(self, idx, line):
        try:
            args = line.split()
            nodelist = args[0].split('=')[1]
            nodes = expand_hostlist(nodelist)
            for node in nodes:
                self.nb[node].add_def(idx)
        except Exception:
            self.results['errors'].append(
                (idx, 'Syntax Error in NodeName directive')
            )

    def _generic_line(self, idx, line):
        if '=' not in line:
            self.results['errors'].append((idx, 'Missing = after parameter'))
        if not line.split('=')[1].strip():
            self.results['errors'].append((idx, 'Missing parameter value'))

    def _partitionname_line(self, idx, line):
        try:
            args = line.split()
            name = args[0].split('=')[1]
            self.nb.partitions[name].append(idx)
            node_params = [
                arg for arg in args if arg.lower().startswith('nodes=')
            ]
            if len(node_params) != 1:
                self.results['errors'].append(
                    idx, 'Missing or repeated Nodes parameter'
                )
            for n_param in node_params:
                nodelist = n_param.split('=')[1]
                if not nodelist:
                    continue
                if nodelist.lower() == 'all':
                    self.nb.allnode_partitions.add(name)
                    continue
                nodes = expand_hostlist(nodelist)
                for node in nodes:
                    self.nb[node].add_partition(name, idx)
        except Exception:
            self.results['errors'].append(
                (idx, 'Syntax Error in PartitionName directive')
            )


class Node:
    """
    Record of a node defined (or not defined) in a slurm file
    containing the line numbers where it is defined, and the partitions
    that it is in with the line definition of those partitions.
    """
    def __init__(self, name):
        self.name = name
        self.deflines = []
        self.partitions = {}

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return str(self) < str(other)

    def add_def(self, line):
        """
        Add a node definition for the given line
        """
        self.deflines.append(line)

    def add_partition(self, partition, line):
        """
        Add a partition for the node at the specified line
        """
        if partition not in self.partitions:
            self.partitions[partition] = [line]
        else:
            self.partitions[partition].append(line)


class NodeBank(dict):
    """
    a NodeBank keeps track of all Nodes encountered in the
    slurm config and works like a defaultdict, automatically
    creating nodes encountered for easy updated. This also
    tracks global information affecting all node records
    such as ALL partitions.

    Also provide error reporting for all nodes defined that
    are either missing partitions or are defined multiple
    times.
    """
    def __init__(self):
        super().__init__()

        self.partitions = defaultdict(list)
        self.allnode_partitions = set()

    def __missing__(self, key):
        if key not in self:
            self[key] = Node(key)
        return self[key]

    def undefined_node_errors(self):
        """
        Report all errors in the form of a list of tuples with line number
        and error messages for nodes that were added to partitions but not
        defined.
        """
        errlines = defaultdict(list)
        for nodename in self:
            node = self[nodename]
            if node.partitions and not node.deflines:
                for lines in node.partitions.values():
                    for line in lines:
                        errlines[line].append(node)
        result = []
        for line, nodes in errlines.items():
            msg_nodes = ', '.join([str(node) for node in sorted(nodes)[:3]])
            if len(nodes) > 3:
                msg_nodes += ', ...'
            msg = 'Undefined nodes added to partition: {0}'.format(msg_nodes)
            result.append((line, msg))

        result.sort()
        return result

    def duplicate_definition_errors(self):
        """
        Report all errors in the form of a list of tuples with line number
        and error messages for nodes that were defined multiple times.
        """
        errlines = defaultdict(list)
        for nodename in self:
            node = self[nodename]
            if len(node.deflines) > 1:
                for line in set(node.deflines):
                    errlines[line].append(node)

        result = []
        for line, nodes in errlines.items():
            msg_nodes = ', '.join([str(node) for node in sorted(nodes)[:3]])
            if len(nodes) > 3:
                msg_nodes += ', ...'
            msg = 'Duplicate node definition: {0}'.format(msg_nodes)
            result.append((line, msg))

        result.sort()
        return result

    def node_missing_partition_errors(self):
        """
        Report all errors in the form of a list of tuples with line number
        and error messages for nodes that were defined but not added to
        a partition.
        """
        if self.allnode_partitions:
            return []

        errlines = defaultdict(list)
        for nodename in self:
            node = self[nodename]
            if node.deflines and not node.partitions:
                for line in node.deflines:
                    errlines[line].append(node)
        result = []
        for line, nodes in errlines.items():
            msg_nodes = ', '.join([str(node) for node in sorted(nodes)[:3]])
            if len(nodes) > 3:
                msg_nodes += ', ...'
            msg = 'Defined node has no partition: {0}'.format(msg_nodes)
            result.append((line, msg))

        result.sort()
        return result
