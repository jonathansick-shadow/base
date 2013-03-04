// -*- lsst-c++ -*-
#ifndef LSST_BASE_ModuleImporter_h_INCLUDED
#define LSST_BASE_ModuleImporter_h_INCLUDED

/**
 *  @file lsst/afw/table/io/ModuleImporter.h
 *
 *  Mechanism for safely importing Python modules from C++; should not be included
 *  except by its own implementation file, the ioLib.i file, and Persistable.cc.
 */

#include <string>

#include "boost/noncopyable.hpp"

namespace lsst { namespace base {

/**
 *  @brief Base class that defines an interface for importing Python modules.
 *
 *  The default implementation (defined in the source file) simply returns
 *  false, indicating that it can't import the given module.  The functional
 *  implementation is in the ioLib Swig module, which is installed when that
 *  module is imported.  That machinery keeps us from calling Python C-API
 *  functions from standalone C++ binaries that aren't linked with Python.
 */
class ModuleImporter : private boost::noncopyable {
public:

    /// Import the given Python module, and return true if successful.
    static bool import(std::string const & name);

    /**
     *  @brief Install the given ModuleImporter in the singleton slot.
     *
     *  The given pointer should point to an instance with static scope.
     */
    static void install(ModuleImporter const * importer);

protected:

    ModuleImporter() {}

    virtual bool _import(std::string const & name) const = 0;

    virtual ~ModuleImporter() {}
};

}} // namespace lsst::base

#endif // !LSST_BASE_ModuleImporter_h_INCLUDED
