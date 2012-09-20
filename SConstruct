# -*- python -*-

from lsst.sconsUtils import scripts, env, targets, utils

scripts.BasicSConstruct.initialize(packageName = "base")

# make lsst64defs.py
import os.path
import re
import subprocess

try:
    import dl
except (ImportError, SystemError):

    # there is no dl module: extract needed constants from system
    def DetermineRtld(context):
        context.Message("Determining RTLD values...")
        result = context.TryRun("""
#include <dlfcn.h>
#include <stdio.h>
int main(void)
{
    printf("%d\\n", RTLD_GLOBAL);
    printf("%d\\n", RTLD_NOW);
    return 0;
}
""", extension=".c")
        if result[0]:
            context.Result("ok")
            return result[1].strip().split("\n")
        utils.Log().fail("Unable to determine RTLD values")

    conf = env.Configure(custom_tests={'DetermineRtld': DetermineRtld,})
    globl, now = conf.DetermineRtld()
    conf.Finish()

    m4flags = "-Dm4_RTLD_GLOBAL=%s -Dm4_RTLD_NOW=%s" % (globl, now)
    r = env.M4("python/lsst64defs.py", "python/lsst64defs.py.m4", M4FLAGS=m4flags)
    targets["python"].extend(r)

scripts.BasicSConstruct.finish()
