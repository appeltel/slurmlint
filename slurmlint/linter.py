"""
This is the linter
"""
from collections import Counter

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
        self.results = {'errors': [], 'nodes': set()}
        self.in_partition = set()
        # generic dispatch for parameters
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

        return self.results

    def _nodename_line(self, idx, line):
        dupes = set()
        try:
            args = line.split()
            nodelist = args[0].split('=')[1]
            nodes = expand_hostlist(nodelist)
            dupes.update(
                [n for n, count in Counter(nodes).items() if count > 1]
            )
            dupes.update(set(nodes).intersection(self.results['nodes']))
            self.results['nodes'].update(nodes)
        #except Exception:
        except RuntimeError:
            self.results['errors'].append(
                (idx, 'Invalid NodeName directive')
            )

        if dupes:
            self.results['errors'].append(
                (idx, 'Duplicate nodes defined: {0}'.format(', '.join(dupes)))
            )

    def _generic_line(self, idx, line):
        if '=' not in line:
            self.results['errors'].append((idx, 'Missing = after parameter'))
        if not line.split('=')[1].strip():
            self.results['errors'].append((idx, 'Missing parameter value'))

    def _partitionname_line(self, idx, line):
        pass
