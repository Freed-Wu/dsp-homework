#! /usr/bin/env python3
from matplotlib import pyplot as plt
import torch
import numpy as np
from scipy.signal import periodogram

x1s = torch.randn(500)
x2s = torch.randn(500)
name = "x"
fig, ax = plt.subplots(num=name)
ax.plot(x1s, label="1st")
ax.plot(x2s, label="2rd")
ax.set_xlabel("$n$")
ax.set_ylabel("$x(n)$")
plt.legend()
plt.savefig(f"images/2/{name}.png")

var_v = 0.27
delta = 0.05
N = 1024
times = 100
hs = np.zeros([N, 2])
x = np.zeros(N)
e = np.zeros([N - 1])
hss = hs.copy()
for _ in range(times):
    hs1 = hs.copy()
    v = np.sqrt(var_v) * np.random.randn(N)
    for i in range(2, N):
        x[i] = -0.1 * x[i - 1] + 0.8 * x[i - 2] + v[i]
    for i in range(1, N - 1):
        xs = np.array([x[i], x[i - 1]])
        e[i - 1] = x[i + 1] - xs.dot(hs1[i - 1, :])
        hs1[i, :] = hs1[i - 1, :] + delta * e[i - 1] * xs
    hss += hs1
hss /= times
name = "a"
fig, ax = plt.subplots(num=name)
ax.plot(range(2, N - 1), hss[2:-1, 0], label="$a_1$")
ax.plot(range(2, N - 1), hss[2:-1, 1], label="$a_2$")
ax.set_xlabel("$n$")
ax.set_ylabel("$a_i(n)$")
plt.legend()
plt.savefig(f"images/2/{name}.png")

p_f = periodogram(v, return_onesided=True)[1]  # type: ignore
p1 = periodogram(hs1[:, 0] - 0.1, return_onesided=True)[1]  # type: ignore
p2 = periodogram(hs1[:, 1] + 0.8, return_onesided=True)[1]  # type: ignore
name = "power_spectrum"
fig, ax = plt.subplots(num=name)
ax.set_xlabel("$n$")
ax.set_ylabel("$e_i(n)$")
ax.plot(p_f, label="$f(n)$")
ax.plot(p1, label="$e_1(n)$")
ax.plot(p2, label="$e_2(n)$")
plt.legend()
plt.savefig(f"images/2/{name}.png")

r = -np.array([-0.5, 0.85])
loss = hss[2:-1] @ r + 0.945
name = "loss"
fig, ax = plt.subplots(num=name)
ax.set_xlabel("$n$")
ax.set_ylabel("$J(n)$")
ax.plot(loss)
plt.savefig(f"images/2/{name}.png")
