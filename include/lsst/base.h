#if !defined(LSST_BASE_BASE_H)
#define LSST_BASE_BASE_H 1
/**
 * @file
 *
 * Basic LSST definitions
 */
#include "boost/shared_ptr.hpp"

/**
 * A shared pointer to an object
 *
 * \note Using this macro is preferable to the Ptr typedef in type T as no definition of T need be provided,
 * a forward definition (<tt>class T;</tt>) is sufficient
 *
 * \sa CONST_PTR
 */
#define PTR(T) boost::shared_ptr<T>
/**
 * A shared pointer to a const object
 *
 * \sa PTR
 */
#define CONST_PTR(T) boost::shared_ptr<T const>

#endif
