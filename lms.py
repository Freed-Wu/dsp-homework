#! /usr/bin/env python3
"""LMS algorithm.

usage: lms.py [-hVn] [-o <dir>] [-f <format>]

options:
    -h, --help              Show this screen.
    -V, --version           Show version.
    -n, --dry-run           Don't open any windows.
    -o, --output <dir>      Save output to a directory.
    -f, --format <format>   Choose saved files' format. [default: png]

format:
    png, jpg, bmp, pdf, eps
"""
import numpy as np


def get_loss(H0, H1):
    """get_loss.

    :param H0:
    :param H1:
    """
    return 0.55 + H0 ** 2 + H1 ** 2 + 2 * H0 * H1 * np.cos(np.pi / 8) \
        - np.sqrt(2) * H0 * np.cos(np.pi / 10) \
        - np.sqrt(2) * H1 * np.cos(9 * np.pi / 40)


def calc_loss(hs0, N: int = 2048):
    """calc_loss.

    :param hs0:
    :param N:
    :type N: int
    """
    hs1 = hs0.copy()
    n = np.arange(N)
    s = np.sqrt(0.05) * np.random.randn(N)
    x = np.sqrt(2) * np.sin(2 * np.pi * n / 16)
    y = np.sin(2 * np.pi * n / 16 + np.pi / 10) + s
    e = np.zeros([N - 1])
    for i in range(1, N):
        xs = np.array([x[i], x[i - 1]])
        e[i - 1] = y[i] - xs.dot(hs1[i - 1, :])
        hs1[i, :] = hs1[i - 1, :] + delta * e[i - 1] * xs
    return s, hs1, e, get_loss(hs1[:, 0], hs1[:, 1])


if __name__ == "__main__" and __doc__:
    from docopt import docopt
    from typing import Dict, Union, List, Any
    Arg = Union[bool, int, str, List[str]]
    args: Dict[str, Arg] = docopt(
        __doc__, version="v0.0.1", options_first=True)

    from matplotlib import pyplot as plt
    from scipy.linalg import toeplitz
    import os
    fmt: str
    if args["--format"] in ["png", "jpg", "bmp", "pdf", "eps"]:
        fmt = args["--format"]  # type: ignore
    else:
        fmt = "png"

    H0, H1 = np.meshgrid(np.arange(-2, 4, 0.1), np.arange(-4, 2, 0.1))
    J = get_loss(H0, H1)
    name = "surface"
    fig = plt.figure(name)
    ax: Any = fig.add_subplot(projection="3d")
    ax.set_xlabel(r"$h_0$")
    ax.set_ylabel(r"$h_1$")
    ax.set_zlabel(r"$J(h)$")
    ax.plot_surface(H0, H1, J)
    if isinstance(args["--output"], str):
        fig.savefig(os.path.join(args["--output"], name + "." + fmt))

    N = 2048
    # steedpest descend {{{ #
    delta = 0.4
    Rxx = toeplitz([1, np.cos(2 * np.pi / 16)])
    Ryx = np.array([1 / np.sqrt(2) * np.cos(np.pi / 10),
                    1 / np.sqrt(2) * np.cos(2 * np.pi / 16 + np.pi / 10)])
    hs = np.zeros([N, 2])
    hs[0, :] = np.array([3, -4])
    hs0 = hs.copy()
    for i in range(N - 1):
        Vg = 2 * Rxx @ hs[i, :] - 2 * Ryx
        hs[i + 1, :] = hs[i, :] - delta * Vg / 2
    # }}} steedpes #
    # LMS {{{ #
    times = 100
    # avoid warning about undefined variables
    s, hs1, e, J1 = calc_loss(hs0, N)
    hs100, J100 = hs1, J1
    for i in range(times - 1):
        s, hs1, e, J1 = calc_loss(hs0, N)
        J100 += J1
        hs100 += hs1
    J100 /= times
    hs100 /= times
    # }}} LMS #

    name = "noise"
    fig = plt.figure(name)
    ax = fig.add_subplot()
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$s(n)$")
    ax.plot(s)
    if isinstance(args["--output"], str):
        fig.savefig(os.path.join(args["--output"], name + "." + fmt))

    name = "error"
    fig = plt.figure(name)
    ax = fig.add_subplot()
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$e(n)$")
    ax.plot(e)
    if isinstance(args["--output"], str):
        fig.savefig(os.path.join(args["--output"], name + "." + fmt))

    name = "loss"
    fig = plt.figure(name)
    ax = fig.add_subplot()
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$J(n)$")
    ax.plot(J1, label="LMS 1")
    ax.plot(J100, label="LMS 100")
    plt.legend()
    if isinstance(args["--output"], str):
        fig.savefig(os.path.join(args["--output"], name + "." + fmt))

    name = "lms"
    fig = plt.figure(name)
    ax = fig.add_subplot()
    ax.set_xlabel(r"$h_0$")
    ax.set_ylabel(r"$h_1$")
    ax.contour(H0, H1, J, 100)
    ax.plot(hs[:, 0], hs[:, 1], label="steepest descend")
    ax.plot(hs1[:, 0], hs1[:, 1], label="LMS")
    ax.plot(hs100[:, 0], hs100[:, 1], label="LMS100")
    plt.legend()
    if isinstance(args["--output"], str):
        fig.savefig(os.path.join(args["--output"], name + "." + fmt))

    if not args["--dry-run"]:
        plt.show()
