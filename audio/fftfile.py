#!/usr/bin/env python3

# record N samples, performs FFT and plots the
# spectrum. Normalization is still TBD

import scard, plot, time, argparse, sys
from collections import namedtuple

import numpy as np
import matplotlib as mpl
mpl.use('macosx')
import matplotlib.pyplot as plt


def main(sc):
    ccplot = plot.plot()

    sf = args.srate

    sp = np.loadtxt(f)

    N = len(sp)
    n = np.arange(N)
    f = n/(N/sf)/2

    ccplot.plotfft(f, [sp])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--srate', type=int, default=192000,
        help='number of samples per second')
    parser.add_argument('--file', type=str, default='',
        help='load data from file')

    args, remaining = parser.parse_known_args()

    main(args)
