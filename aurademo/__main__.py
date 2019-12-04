# -*- coding: utf-8 -*-

"""__main__: executed when invoking aurademo cmd."""

import traceback, os, base64
from optparse import OptionParser
from distutils.version import LooseVersion
#from aurademo import _version, main
from aurademo import main
_version = "0.1"

import os, uuid, ConfigParser, sys

def cli():
    desc = """Turnkey demo setup"""
    optversion = "%prog" +" %s" % _version
    parser = OptionParser(usage="USAGE: %prog [options] ini0 [.. iniN]", description=desc, version=optversion)
    parser.add_option("--verbose", dest="verbose", default=False, action="store_true", help="be verbose [default: %default]")
    parser.add_option("--workdir", dest="workdir", default="aurademo", help="working dir prefix [default : %default]")
    (options, files) = parser.parse_args()

    if not os.path.exists(options.workdir):
        os.makedirs(options.workdir)

    if len(files)==0:
        parser.error("no ini file(s) specified")

    for configF in files:
        if not os.path.exists(os.path.expanduser(configF)):
            parser.error("%s does not exist" % configF)

    ini = ConfigParser.RawConfigParser()
    ini.read(files)
    cfg={}
    cfg["__ordered__"] = ini.sections()
    for section in ini.sections():
        inioptions = {}
        for o in ini.options(section):
            inioptions[o] = ini.get(section,o)

        cfg[section] = inioptions
        
        inioptions["__name__"] = section

        if "gwc" in inioptions:
            inioptions["setupscript"]="gwcsetupscript.sh"

        if "setupscript" not in inioptions:
            parser.error("%s missing setupscript option. Please provide 'setupscript=<pathtoscript>'" % section)

        # use defaults if values not specified in ini file(s)
        inioptions["box"] = inioptions.get("box","centos/7")
        inioptions["memory"] = inioptions.get("memory","1024")
        if 'network' in inioptions:
            inioptions["network"] = '%s.vm.network "public_network", %s'% (section,inioptions['network'])
        else:
            inioptions["network"] = "no bridge network"

        if "vpnfilename" in inioptions:
            with open((os.path.expanduser(inioptions["vpnfilename"])),"r") as f:
                cfg["vpnbuf"] = base64.b64encode(f.read())
        
    return options, cfg

def __entrypoint__():
    try:
        options, cfg = cli()
        main(options,cfg)
    except KeyboardInterrupt, e:
        print "Goodbye"
        sys.exit(1)
    except EnvironmentError, e:
        print "Fatal: %s" %e
        sys.exit(1)
    except Exception, e:
        traceback.print_exc()
        print e
        sys.exit(1)

if __name__ == "__main__":
    __entrypoint__()
