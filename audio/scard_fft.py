#!/usr/bin/env python3

# record N samples, performs FFT and plots the
# spectrum. Normalization is still TBD

import scard, plot, time, argparse, sys
from collections import namedtuple

import numpy as np
import matplotlib as mpl
mpl.use('macosx')
import matplotlib.pyplot as plt


def main(sc, rounds):
    cc = np.zeros(96001)
    ccplot = plot.plot()

    sf = sc.input.samplerate
    t = np.arange(sc.input.samples)/sf

    rec = sc.record()

    sp1 = np.fft.rfft(rec[0])
    sp2 = np.fft.rfft(rec[1])

    N = len(sp1)
    n = np.arange(N)
    f = n/(N/sf)/2

    ccplot.plotfft(f, [np.abs(sp1), np.abs(sp2)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-l', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument('--device', type=str, default='Scarlett',
        help='device index')
    parser.add_argument('--channels', type=int, default=1,
        help='number of channels to record (1 or 2)')
    parser.add_argument('--srate', type=int, default=192000,
        help='number of samples per second')
    parser.add_argument('--samples', type=int, default=192000,
        help='number of samples to capture')
    parser.add_argument('--norm', type=float, default=1.0,
        help='normalization (to 1V)')

    args, remaining = parser.parse_known_args()

    assert args.srate == args.samples
    assert args.channels == 1 or args.channels == 2

    if args.l:
        scard.query_devices()
        parser.exit(0)

    input = scard.input(args.device, args.srate, args.samples, args.channels, args.norm)
    scard = scard.scard(input)

    main(scard, args.rounds)
