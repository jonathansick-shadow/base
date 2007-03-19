# -*- python -*-
#
# Setup our environment
#
import glob
import sys
import os

# ensure that we can find SConsUtils
#
if not os.environ.has_key("SCONSUTILS_DIR"):
    raise Exception("SCONSUTILS_DIR: environment variable not set")
sys.path = [ "%s/python" % os.environ["SCONSUTILS_DIR"] ] + sys.path 
import lsst.SConsUtils as scons

env = scons.MakeEnv("core",
                    r"$HeadURL$")

#
# Install things
#

# files to ignore when copying files into installation dir
#
env['IgnoreFiles'] = r"(~$|\.pyc$|^\.svn$)"

# on installation, copy the python directory to the install dir
#
Alias("install", env.Install(env['prefix'], "python"))

# on installation, copy the ups directory to the install dir
#
Alias("install", env.InstallEups(env['prefix'] + "/ups",
                                 glob.glob("ups/*.table")))
# declare this package
# 
env.Declare()

env.Help("""
A package that provides the lsst python module which includes a custom
loader.  
""")
