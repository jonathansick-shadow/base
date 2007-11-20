# -*- python -*-
#
# Setup our environment
#
import glob
import sys
import os
import re

# ensure that we can find SConsUtils
#
if not os.environ.has_key("SCONSUTILS_DIR"):
    raise Exception("SCONSUTILS_DIR: environment variable not set")
sys.path = [ "%s/python" % os.environ["SCONSUTILS_DIR"] ] + sys.path 
import lsst.SConsUtils as scons

env = scons.MakeEnv("core",
                    r"$HeadURL$")

# make lsst64defs.py
try:
    import dl
except (ImportError, SystemError):

    # there is no dl module: extract needed constants from system
    dlfcn = open("/usr/include/bits/dlfcn.h", 'r')
    rtld = filter(lambda x: re.search(r'RTLD_GLOBAL|RTLD_NOW', x),
                  dlfcn.readlines())
    dlfcn.close()
    globl = filter(lambda x: re.search(r'#define\s+RTLD_GLOBAL', x), rtld)
    if len(globl) == 0:
        raise Error("No definition for RTLD_GLOBAL found")
    globl = re.sub(r'^.*#define\s+RTLD_GLOBAL\s+', '', globl[0])
    globl = re.sub(r'\s+.*$', '', globl)

    now =  filter(lambda x: re.search(r'#define\s+RTLD_NOW', x), rtld)
    if len(now) == 0:
        raise Error("No definition for RTLD_NOW found")
    now = re.sub(r'^.*#define\s+RTLD_NOW\s+', '', now[0])
    now = re.sub(r'\s+.*$', '', now)

    m4flags = "-Dm4_RTLD_GLOBAL=%s -Dm4_RTLD_NOW=%s" % (globl, now)
    env.M4("python/lsst64defs.py", "python/lsst64defs.py.m4", M4FLAGS=m4flags)
    
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
