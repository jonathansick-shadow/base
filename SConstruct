# -*- python -*-

from lsst.sconsUtils import scripts, env, targets

scripts.BasicSConstruct.initialize(packageName = "base")

# make lsst64defs.py
import os.path
import re

try:
    import dl
except (ImportError, SystemError):

    # there is no dl module: extract needed constants from system
    dlfcn = None
    for dir in ["/usr/include/bits", "/usr/include"]:
        incFile = os.path.join(dir, "dlfcn.h")
        if os.path.exists(incFile):
            dlfcn = open(incFile, 'r')
            break

    if not dlfcn:
        raise RuntimeError("Unable to find dlfcn.h")

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
    r = env.M4("python/lsst64defs.py", "python/lsst64defs.py.m4", M4FLAGS=m4flags)
    targets["python"].extend(r)

scripts.BasicSConstruct.finish()
