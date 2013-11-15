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
import os.path
import pkgutil

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
    '''
    if dlflags != 0:
        #sys.setdlopenflags(dlflags)
        pass
    '''
except ImportError:
    sys.stderr.write(
        "Could not import lsst64defs; please ensure the base package has been built (not just setup).\n"
    )

class SwiggedImporter(object):
    def find_module(self, fullname, path=None):
        if fullname.endswith('Lib'):
            self.path = path
            return self
        return None
        
    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]  #already loaded
        #imp.find_module doesn't do recursive nested imports, but thanks
        #to pkgutil.extend_path, the path should include all levels.
        #Just load the final module
        part = name.split('.')[-1] 
        module_info = imp.find_module(part, self.path)

        #Set the flags
        sys.setdlopenflags(DLFLAGS)
        module = imp.load_module(name, *module_info)
        #Re-set flags to original
        sys.setdlopenflags(ORIGDLFLAGS)
        sys.modules[name] = module
        return module

sys.meta_path = [SwiggedImporter()]



try:
    import lsstcppimport
except ImportError:
        sys.stderr.write(
        "Could not import lsstcppimport; please ensure the base package has been built (not just setup).\n"
    )
