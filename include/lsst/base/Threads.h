#include <stdexcept>

namespace lsst {
namespace base {

extern bool const haveOpenBlas;

class NoOpenBlasException : public std::runtime_error {
public:
    NoOpenBlasException() : std::runtime_error("OpenBLAS is not available") {};
};

void setThreads(unsigned int numThreads);
unsigned int getThreads();

}} // namespace lsst::base
