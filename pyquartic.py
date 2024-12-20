"""
Modified Ferrari's quartic solver and modified Cardano's cubic solver for Python (4th and 3rd order polynomials)
Using modified algorithms from: https://quarticequations.com
Functions can optionally be 'numbarized' by just installing numba
Python implementation by: mzivic7
Source code: https://github.com/mzivic7/pyquartic
Issues: https://github.com/mzivic7/pyquartic/issues
Licence: GNU General Public License v3.0
"""


import cmath
import math

try:
    from numba import complex128, float64, njit
    from numba.types import UniTuple
    numba_avail = True
except ImportError:
    numba_avail = False


# constants
sq3 = math.sqrt(3)
pi23 = 2 * math.pi / 3


def solve_cubic(a, b, c, d):
    """Solves cubic equation with modified Cardano's method.
    az^3 + bz^2 + cz + d = 0
    Uses modified Cardano's method from 'Numerical Recipes' and Viète’s trigonometric method to avoid large error in ceratin cases.
    https://quarticequations.com/Cubic.pdf"""

    # convert to depressed form
    a2, a1, a0 = b/a, c/a, d/a

    q = a1/3 - a2**2/9
    r = (a1*a2-3*a0)/6 - a2**3/27
    rq = r**2 + q**3
    if rq > 0:
        # Numerical Recipes algorithm
        aa = (abs(r) + math.sqrt(rq))**(1/3)
        if r >= 0:
            t = aa - q / aa
        else:
            t = q/aa - aa
        z1 = t - a2/3
        x = -t/2 - a2/3
        y = (sq3/2) * (aa + (q/aa))
        z2 = complex(x, y)
        z3 = complex(x, -y)
    else:
        # Viète algorithm
        if q == 0:
            theta = 0
        elif q < 0:
            theta = math.acos(r/(-q)**(3/2))

        # repeating stuff
        m = 2 * math.sqrt(-q)
        n = a2/3

        # solutions
        phi1 = theta / 3
        phi2 = phi1 - pi23
        phi3 = phi1 + pi23
        z1 = complex(m * math.cos(phi1) - n)
        z2 = complex(m * math.cos(phi2) - n)
        z3 = complex(m * math.cos(phi3) - n)
    return (z1, z2, z3)


def solve_cubic_one(a, b, c):
    """Calculates only one real root for depressed cubic equation.
    z^3 + az^2 + bz + c = 0
    Uses modified Cardano's method from 'Numerical Recipes' and Viète’s trigonometric method to avoid large error in ceratin cases.
    https://quarticequations.com/Cubic.pdf"""

    q = b/3 - a**2/9
    r = (b*a-3*c)/6 - a**3/27
    rq = r**2 + q**3
    if rq > 0:
        # Numerical Recipes algorithm
        aa = (abs(r) + math.sqrt(rq))**(1/3)
        if r >= 0:
            t = aa - q/aa
        else:
            t = q/aa - aa
        z1 = t - a/3
    else:
        # Viete algorithm
        if q == 0:
            theta = 0
        elif q < 0:
            theta = math.acos(r/(-q)**(3/2))
        fi = theta/3
        z1 = 2 * math.sqrt(-q) * math.cos(fi) - a/3
    return z1


def solve_quartic(a, b, c, d, e):
    """Solves quartic equation with modified Ferrari's method.
    az^4 + bz^3 + cz^2 + dz + e = 0
    https://quarticequations.com/Quartic2.pdf"""

    # convert to depressed form
    a3, a2, a1, a0 = b/a, c/a, d/a, e/a

    cc = a3/4
    b2 = a2 - 6*cc**2
    b1 = a1 - 2*a2*cc + 8*cc**3
    b0 = a0 - a1*cc + a2*cc**2 - 3*cc**4

    # one real root of Ferrari's resolvent cubic
    y = solve_cubic_one(b2, b2**2/4 - b0, -b1**2/8)
    y = max(y, 0)

    s = y**2 + b2*y + b2**2/4 - b0
    # protection from root of negative number
    if s > 0:
        if b1 < 0:
            r = -math.sqrt(s)
        else:
            r = math.sqrt(s)
    else:
        r = float("nan")

    # repeating stuff
    p = cmath.sqrt(y/2) - cc
    p1 = -cmath.sqrt(y/2) - cc
    q = -y/2 - b2/2

    # solutions to depressed quartic equation
    z1 = p + cmath.sqrt(q - r)
    z2 = p - cmath.sqrt(q - r)
    z3 = p1 + cmath.sqrt(q + r)
    z4 = p1 - cmath.sqrt(q + r)
    return (z1, z2, z3, z4)


# if numba is available, compile functions ahead of time
if numba_avail:
    jitkw = {"cache": True}
    solve_cubic = njit(UniTuple(complex128, 3)(float64, float64, float64, float64), **jitkw)(solve_cubic)
    solve_cubic_one = njit(float64(float64, float64, float64), **jitkw)(solve_cubic_one)
    solve_quartic = njit(UniTuple(complex128, 4)(float64, float64, float64, float64, float64), **jitkw)(solve_quartic)
