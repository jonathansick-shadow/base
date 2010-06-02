/*
 * Check that the PTR and CONST_PTR macros work, even with embedded commas
 */
#include "lsst/base.h"

class Foo;

template<typename T, typename U>
class Goo {
};

int main() {
    PTR(Foo) pf;
    CONST_PTR(Foo) cpf;

    PTR(Goo<int, int>) pg;
    PTR(Goo<int, Goo<float, float> const &>) cpg;
}
