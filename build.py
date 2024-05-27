from numba.pycc import CC
from numba import njit, float64, complex128
from numba.types import UniTuple
import pyquartic

cc = CC('pyquartic')
cc.verbose = True

cc.export('solve_cubic', UniTuple(complex128, 3)(float64, float64, float64, float64))(pyquartic.solve_cubic)
cc.export('solve_cubic_one', float64(float64, float64, float64))(pyquartic.solve_cubic_one)
cc.export('solve_quartic', UniTuple(complex128, 4)(float64, float64, float64, float64, float64))(pyquartic.solve_quartic)

if __name__ == "__main__":
    cc.compile()

