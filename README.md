# pyquartic
Modified Ferrari's quartic solver and modified Cardano's cubic solver for Python (4th and 3rd order polynomials).  

## Features
- Original algorithms are modified so they provide stable and correct solutions to polynomials  
- Using modified algorithms from [quarticequations.com](https://quarticequations.com)
- Functions are optimized for fast computing (up to 20x faster than np.roots)  
- Functions can optionally be 'numbarized' to be much faster  

## Usage
Cubic and quartic solvers are located in [pyquartic.py](pyquartic.py).  
Numba is optional. It is auto detected, so it just needs to be installed.  
If numba is available, functions will be compiled ahead of time, with caching enabled.  
[pyquartic_nonumba.py](pyquartic_nonumba.py) can be used in case where numba is available but should not be used.  
Numpy is required only in tests for comparison with np.roots().  
Outputs data are complex numbers in tuple.  

### Cubic solver
```
import pyquartic
coefs = (a, b, c, d)
roots = pyquartic.solve_cubic(*coefs)
```
Where `a, b, c, d` are cubic equation coefficients:  
$`ax^3 + bx^2 + cx + d = 0`$

### Quartic solver
```
import pyquartic
coefs = (a, b, c, d, e)
roots = pyquartic.solve_quartic(*coefs)
```
Where `a, b, c, d, e` are quartic equation coefficients:  
$`ax^4 + bx^3 + cx^2 + dx + e = 0`$

## Speed analysis
Speed analysis can be performed by running [test_pyquartic.py](test_pyquartic.py).
Note that test requires numpy, for comparison with numpy's solver.  
Numpy's polyroots solver computes eigenvalues of a companion matrix, formed from n-th order polynomial coefficients. This method is stable and accurate, but very slow and is not supported by numba.
Tests are performed on large number of coefficients (10000) where coefficients range from -10000 to 10000, times shown are mean and best times from those iterations.  
Provided are three tests for cubic and quartic: numpy's polyroots, modified Ferrari's algorithm, and 'numbarized' modified Ferrari's algorithm.  
```
Cubic
np.root: 113.7076 us, best: 105.672 us
nonumba: 14.3613 us, best: 13.075 us
cardano: 5.628 us, best: 5.095 us
```
```
Quartic
np.root: 116.1679 us, best: 108.099 us
nonumba: 21.0779 us, best: 18.921 us
ferrari: 6.4158 us, best: 5.805 us
```

## Modifications to algorithms
Much more detailed versions and tutorials for this modifications are covered in this paper: [quarticequations.com](https://quarticequations.com).  
This project is just implementation of there described modified algorithms.  

### Cardano's method
Cardano's method has large round-off error at some specific cases (when parameter q approaches zero).  
While mathematically correct, when calculated on computer where numbers are rounded to n decimals, this can create large errors, that are later carried to quartic solver.  
To fix this, solution from 'Numerical Recipes' is used for case when there is only one real solution.  
When there are three real solutions, Viète’s trigonometric method is used.  
More details [here](https://quarticequations.com/Cubic.pdf).  

### Ferrari's method
Ferrari's method uses one real root from cubic equation solved with Cardano's method.  
As this root approaches zero, algorithm becomes computationally unstable due to round-off error.  
Modified algorithm is 'modern generalization of Cardano’s Problem VIII', it avoids this instability by adding one more calculation.  
More details [here](https://quarticequations.com/Quartic2.pdf).  

## Building binaries
This is only for numba compiled binaries. This way numba pyquartic can be imported and used without need of having numba installed after building.  
Numba and setuptools must be installed only during building: `pip install numba setuptools`.  
Run: `python -m build`. This will generate .so file, one can copy it, and use `import pyquartic`.  

## Requirements
- Python 3.x.x
- math
- cmath
- numba (optional)
- setuptools (for compiling numba binary)
- numpy (for testing)
