import time

import numpy as np

import pyquartic
import pyquartic_nonumba

time1 = []
time2 = []
time3 = []

rng = np.random.default_rng()

for i in range(1000):
    coef = rng.uniform(-10000, 10000, 4)
    coef_inv = coef[::-1]

    start = time.perf_counter()
    roots1 = np.polynomial.polynomial.polyroots(coef_inv)
    time1.append((time.perf_counter() - start))

    start = time.perf_counter()
    roots2 = pyquartic_nonumba.solve_cubic(*coef)
    time2.append((time.perf_counter() - start))

    start = time.perf_counter()
    roots3 = pyquartic.solve_cubic(*coef)
    time3.append((time.perf_counter() - start))

print()
print("Cubic")
print(f"np.root: {round(np.array(time1).mean()*1000000, 4)} us, best: {round(np.array(time1).min()*1000000, 4)} us")
print(f"nonumba: {round(np.array(time2).mean()*1000000, 4)} us, best: {round(np.array(time2).min()*1000000, 4)} us")
print(f"cardano: {round(np.array(time3).mean()*1000000, 4)} us, best: {round(np.array(time3).min()*1000000, 4)} us")


time4 = []
time5 = []
time6 = []
for i in range(100000):
    coef = rng.uniform(-10000, 10000, 5)
    coef_inv = coef[::-1]

    start = time.perf_counter()
    roots4 = np.polynomial.polynomial.polyroots(coef_inv)
    time4.append((time.perf_counter() - start))

    start = time.perf_counter()
    roots5 = pyquartic_nonumba.solve_quartic(*coef)
    time5.append((time.perf_counter() - start))

    start = time.perf_counter()
    roots6 = pyquartic.solve_quartic(*coef)
    time6.append((time.perf_counter() - start))

print()
print("Quartic")
print(f"np.root: {round(np.array(time4).mean()*1000000, 4)} us, best: {round(np.array(time4).min()*1000000, 4)} us")
print(f"nonumba: {round(np.array(time5).mean()*1000000, 4)} us, best: {round(np.array(time5).min()*1000000, 4)} us")
print(f"ferrari: {round(np.array(time6).mean()*1000000, 4)} us, best: {round(np.array(time6).min()*1000000, 4)} us")
