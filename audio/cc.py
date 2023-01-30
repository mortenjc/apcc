#!/usr/bin/env python3

# Record M rounds of N samples from two channels
# Perform cross correllation and ploit the spectrum
# normalization is still TBD

import scard, plot, time, argparse, sys
from collections import namedtuple
from datetime import datetime as dt

import numpy as np
import matplotlib as mpl
mpl.use('macosx')
import matplotlib.pyplot as plt


def save(data, sc, rounds):
    now = dt.now()
    filename = f'cc_{now.strftime("%H%M%S")}_rounds_{rounds}.csv'
    header = 'rate {}, samples {}, rounds {}, norm {}'.format(
    sc.input.samplerate, sc.input.samples, rounds, sc.input.norm)

    with open(filename, 'w') as my_file:
        for i in data:
            np.savetxt(my_file, i, header=header)


def main(sc, rounds):
    cc = np.zeros(96001)
    ccplot = plot.plot()


    sf = sc.input.samplerate
    t = np.arange(sc.input.samples)/sf

    for r in range(rounds):
        print(f'round {r}')
        rec = sc.record(sc.input.norm)

        sp1 = np.fft.rfft(rec[0])/sc.input.samples
        sp2 = np.fft.rfft(rec[1])/sc.input.samples
        cc = cc + sp1 * np.conjugate(sp2)

    cc = np.sqrt(abs(cc))/rounds

    N = len(sp1)
    n = np.arange(N)
    f = n/(N/sf)/2

    save([cc], sc, rounds)
    ccplot.plotfft(f, [cc])



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
    parser.add_argument('--rounds', type=int, default=1,
        help='number of cc rounds')

    args, remaining = parser.parse_known_args()

    assert args.srate == args.samples
    channels = 2

    if args.l:
        scard.query_devices()
        parser.exit(0)

    input = scard.input(args.device, args.srate, args.samples, channels, args.norm)
    scard = scard.scard(input)

    main(scard, args.rounds)
