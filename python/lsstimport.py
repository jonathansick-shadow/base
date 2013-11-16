#! env python

# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#

#
import sys
import imp
import functools
import os.path

# Ensure that duplicate allocations--particularly those related to RTTI--are
# resolved by setting dynamical library loading flags.
RTLD_GLOBAL = -1
RTLD_NOW = -1
ORIGDLFLAGS = sys.getdlopenflags()
try:
    import dl
    if hasattr(dl, 'RTLD_GLOBAL'):  RTLD_GLOBAL = dl.RTLD_GLOBAL
    if hasattr(dl, 'RTLD_NOW'):     RTLD_NOW    = dl.RTLD_NOW
except ImportError:
    # 64bit linux does not have a dl module...
    pass
except SystemError:
    # ...if it does it should throw a SystemError
    pass

try:
    if RTLD_GLOBAL < 0:
        import lsst64defs
        RTLD_GLOBAL = lsst64defs.RTLD_GLOBAL   # usually 0x00100
    if RTLD_NOW < 0:
        import lsst64defs
        RTLD_NOW = lsst64defs.RTLD_NOW         # usually 0x00002
    DLFLAGS = RTLD_GLOBAL|RTLD_NOW
except ImportError:
    sys.stderr.write(
        "Could not import lsst64defs; please ensure the base package has been built (not just setup).\n"
    )

orig_imp_load_module = imp.load_module
@functools.wraps(orig_imp_load_module)
def imp_load_module(name, *args):
    pathParts = args[1].split(os.path.sep)
    #Find all swigged LSST libs.  Does _lsstcppimport need to be wrapped?
    if 'lsst' in pathParts[:-1] and pathParts[-1].startswith('_') and \
            (pathParts[-1].endswith('.so') or pathParts[-1].endswith('.dylib')):
        #Set flags
        sys.setdlopenflags(DLFLAGS)
        try:
            module = orig_imp_load_module(name, *args)
        finally:
            #Set original flags
            sys.setdlopenflags(ORIGDLFLAGS)
    else:
        module = orig_imp_load_module(name, *args)
    return module
imp.load_module = imp_load_module

try:
    import lsstcppimport
except ImportError:
        sys.stderr.write(
        "Could not import lsstcppimport; please ensure the base package has been built (not just setup).\n"
    )
