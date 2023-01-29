#!/usr/bin/env python3

# Record N samples from uSB sounddevice and plot the
# samples (amplitude) as function of time

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
    ccplot.plotamp(t, rec, 'a(t)')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-l', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument('--device', type=str, default='Scarlett',
        help='device index')
    parser.add_argument('--srate', type=int, default=192000,
        help='number of samples per second')
    parser.add_argument('--samples', type=int, default=192000,
        help='number of samples to capture')
    parser.add_argument('--norm', type=float, default=1.0,
        help='normalization (to 1V)')

    args, remaining = parser.parse_known_args()

    assert args.srate == args.samples
    channels = 2

    if args.l:
        scard.query_devices()
        parser.exit(0)

    input = scard.input(args.device, args.srate, args.samples, channels, args.norm)
    scard = scard.scard(input)

    main(scard, args.rounds)
