#include "lsst/base/Threads.h"
#include <dlfcn.h>
#include <cstddef>
#include <cstdlib>

#include <iostream>


#ifndef RTLD_DEEPBIND // Non-POSIX flag, so it may not exist
#define RTLD_DEEPBIND 0 // Will be ignored
#endif

namespace lsst {
namespace base {

namespace {

typedef int (*Getter)(void);
typedef void (*Setter)(int);

Getter getBlasThreads = NULL;
Setter setBlasThreads = NULL;

bool loadOpenBlas() {
    if (haveOpenBlas) {
        return true;
    }

    void* openblas = dlopen("libopenblas.so", RTLD_LAZY | RTLD_LOCAL | RTLD_DEEPBIND);
    if (!openblas) return false;

    // Believe it or not, the function which returns the number of threads that OpenBLAS will actually use is
    // called "goto_get_num_procs". The number returned by THIS function, and not "openblas_get_num_threads"
    // nor "openblas_get_num_procs", is modified by calls to "openblas_set_num_threads". Confused? Me too.
    (void*&)getBlasThreads = dlsym(openblas, "goto_get_num_procs");
    (void*&)setBlasThreads = dlsym(openblas, "openblas_set_num_threads");
    return getBlasThreads && setBlasThreads;
}

bool disableOpenBlasThreadingUnlessExplicit()
{
    if (!std::getenv("OPENBLAS_NUM_THREADS") &&
        !std::getenv("GOTO_NUM_THREADS") &&
        !std::getenv("OMP_NUM_THREADS") &&
        haveOpenBlas &&
        !std::getenv("LSST_ALLOW_IMPLICIT_OPENBLAS")
        ) {
        unsigned int const numThreads = getBlasThreads();
        if (numThreads > 1) {
            std::cerr << "WARNING: You are using OpenBLAS with multiple threads (" << numThreads <<
                "), but have not\n" <<
                "specified the number of threads using one of the OpenBLAS environment variables\n" <<
                "(OPENBLAS_NUM_THREADS, GOTO_NUM_THREADS, OMP_NUM_THREADS). This may indicate\n" <<
                "that you are unintentionally using multiple threads, which may cause problems\n"
                "with multiprocessing. WE HAVE THEREFORE DISABLED OPENBLAS THREADING. If you know\n" <<
                "what you are doing and want OpenBLAS threads enabled, set the environment\n" <<
                "variable LSST_ALLOW_IMPLICIT_OPENBLAS ." << std::endl;
            setBlasThreads(1);
            return true;
        }
    }
    return false;
}

} // anonymous namespace

extern bool const haveOpenBlas = loadOpenBlas();
static bool disabled = disableOpenBlasThreadingUnlessExplicit();

void setThreads(unsigned int numThreads)
{
    if (!haveOpenBlas) {
        throw NoOpenBlasException();
    }
    setBlasThreads(numThreads);
}

unsigned int getThreads()
{
    if (!haveOpenBlas) {
        throw NoOpenBlasException();
    }
    return getBlasThreads();
}

}} // namespace lsst::base
