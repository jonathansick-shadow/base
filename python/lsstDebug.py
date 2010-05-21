#
# Define a class to configure debugging information
#
class Info(object):
    """An object cognisant of debugging parameters appropriate for module "name"; any request for a value
will return False unless that value has been set, either in the module or as an attribute of this object.

E.g.
    import lsstDebug

    display = lsstDebug.Info(__name__).display
will set display to False, unless display has been set:
    display = True
    print lsstDebug.Info(__name__).display
will print True; this is equivalent to
    lsstDebug.Info(__name__).display = True
    print lsstDebug.Info(__name__).display

Why is this interesting?  Because you can replace lsstDebug.Info with your own version, e.g.

import lsstDebug

def DebugInfo(name):
    di = lsstDebug.getInfo(name)        # N.b. lsstDebug.Info(name) would call us recursively
    if name == "foo":
        di.display = True
        
    return di
    
lsstDebug.Info = DebugInfo
"""
    def __init__(self, modname):
        import sys
        self.__dict__["_dict"] = sys.modules[modname].__dict__
        self._modname = modname

    def __getattr__(self, what):
        """Return the value of the variable "what" in self.__modname if set, else False"""
        return self._dict.get(what, False)

    def __setattr__(self, what, value):
        """Set the value of the variable "what" in self.__modname to value"""
        self._dict[what] = value

getInfo = Info
