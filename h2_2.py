#! /usr/bin/env python3
from matplotlib import pyplot as plt
import numpy as np
from padasip.preprocess import input_from_history
from padasip.filters import AdaptiveFilter
name = "relevant"
fig, ax = plt.subplots(num=name)
ax.stem(0.5 * np.cos(0.05 * np.pi * np.arange(10)), label="$r_{x_1}(n)$")
ax.stem([6, 4, 1], linefmt="r", markerfmt="rx", label="$r_{x_2}(n)$")
ax.set_xlabel("$n$")
ax.set_ylabel("$r_{x_i}(n)$")
plt.legend()
plt.savefig(f"images/2/{name}.png")

L = 50000
x1 = np.sin(0.05 * np.pi * np.arange(L))
e = np.random.randn(L)
x2 = e + 2 * np.roll(e, 1) + np.roll(e, 2)
x = x1 + x2
N = 400
X = input_from_history(x, n=N)
lms = AdaptiveFilter(n=N, mu=4e-6, w="zeros")
x1_hat, e_hat, hs = lms.run(x1[N - 1:], X)
x2_hat = x[N - 1:] - x1_hat

name = "x1"
fig, ax = plt.subplots(num=name)
ax.plot(range(L - 50, L), x1_hat[-50:], label="$\hat{x}_1(n)$")
ax.plot(range(L - 50, L), x1[-50:], label="$x_1(n)$")
ax.set_xlabel("$n$")
ax.set_ylabel("$x_1(n)$")
plt.legend()
plt.savefig(f"images/2/{name}.png")

name = "x2"
fig, ax = plt.subplots(num=name)
ax.plot(range(L - 50, L), x2_hat[-50:], label="$\hat{x}_2(n)$")
ax.plot(range(L - 50, L), x2[-50:], label="$x_2(n)$")
ax.set_xlabel("$n$")
ax.set_ylabel("$x_2(n)$")
plt.legend()
plt.savefig(f"images/2/{name}.png")
