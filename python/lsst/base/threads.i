// -*- lsst-c++ -*-

%define threads_DOCSTRING
"
Access to the threading functions
"
%enddef

%feature("autodoc", "1");
%module(package="lsst.base.threads", docstring=threads_DOCSTRING) threads

%{
#include "lsst/base/Threads.h"
%}

%include "lsst/base/Threads.h"
