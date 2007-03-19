#! env python
#
import sys
import os.path

import imp

class LSSTImporter:
    """An importer to go on sys.meta_path that enables you to
    find a sub-module anywhere on sys.path, regardless of where its parent
    module was loaded from (requires python 2.5; cf PEP 302).

    More precisely, this importer is not restricted to loading a sub-module
    from a subdirectory of the directory where its parent module was loaded
    from.  Thus, if your sys.path contains multiple directories that contain
    an "lsst" module, then a submodule "lsst.foo" can appear below any of 
    those directories.
    """

    def __init__(self):
        self.isLSSTImporter = True 
        pass

    def find_module(self, fullname, path = None):
        """Find a module in the search path"""

        name = fullname.split(".")[-1]

        for d in sys.path:
            dirname = os.path.join(d, apply(os.path.join, fullname.split(".")))
                                            
            if os.path.isabs(dirname) and os.path.isdir(dirname):
                (fd, filename, desc) = \
                           imp.find_module(name, [os.path.dirname(dirname)])
                return LSSTLoader(fd, filename, desc)

        return None

class LSSTLoader:

    def __init__(self, fd, filename, desc):
        self._fd = fd
        self._filename = filename
        self._desc = desc

    def load_module(self, fullname):
        """Load a module, using the information from an importer's
        find_module"""
        fd = self._fd;             self._fd = None
        filename = self._filename; self._filename = None
        desc = self._desc;         self._desc = None

        return imp.load_module(fullname, fd, filename, desc)

sys.meta_path += [LSSTImporter()]
