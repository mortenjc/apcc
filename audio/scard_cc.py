#!/usr/bin/env python3

import time, argparse, sys
import sounddevice as sd
import numpy as np
import matplotlib as mpl
mpl.use('macosx')
import matplotlib.pyplot as plt

mpl.rcParams['text.color'] = 'green'
mpl.rcParams['axes.labelcolor'] = 'green'
mpl.rcParams['xtick.color'] = 'green'
mpl.rcParams['ytick.color'] = 'green'


def plot_setup():
    #plt.ion()

    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor("black")
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_color('green')

    return fig, ax




def main(args):
    device = args.device
    samplerate = args.samplerate
    nsamples = args.samples
    channels = args.channels

    assert channels == 2

    cc = np.zeros(96001)

    sd.default.channels = 1
    sd.default.samplerate = samplerate

    device_info = sd.query_devices(device, 'input')
    #print(device_info)

    sf = samplerate
    t = np.arange(nsamples)/sf

    for r in range(args.rounds):
        print(f'round {r}')
        rec = sd.rec(nsamples, samplerate=sf, channels=channels)
        sd.wait()

        c1 = [x[0] for x in rec]
        c2 = [x[1] for x in rec]

        assert len(c1) == nsamples
        assert len(c2) == nsamples

        # if args.raw:
        #     print(rec.shape)
        #     print(f'len(rec): {len(rec)}')
        #     print(rec)
        #     print(c1[:10])
        #     print(c2[:10])
        #     sys.exit(0)

        sp1 = np.fft.rfft(c1)
        sp2 = np.fft.rfft(c2)
        print(sp1)

        cc = cc + sp1 * np.conjugate(sp2)


    N = len(sp1)
    n = np.arange(N)
    T = N/sf
    f = n/T/2


    fig, ax = plot_setup()

    # textstr = f'f {maxfreq:7.1f} Hz\nampl {maxval:3.1f}'
    #
    # props = dict(boxstyle='round', facecolor='black', alpha=0.5)
    # ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
    #     verticalalignment='top', bbox=props)


    ax.set_title(f'sample freq {sf} (Hz)', color='green')

    if args.timeplot:
        print(t)
        print(rec)
        amp = [x[0] for x in rec]
        print(amp)
        plt.plot(t, c1, color='green')
        plt.plot(t, c2, color='blue')
        plt.xlabel('t (s)', color='green')
        plt.xlim(0.0, 1.0)
    else:
        plt.plot(f, np.abs(sp1), color='green')
        plt.plot(f, np.abs(sp2), color='blue')
        plt.plot(f, np.sqrt(np.abs(cc))/args.rounds, color='red')
        plt.xlim(1.0, 22000)
        ax.set_xscale('log')
        ax.set_yscale('log')
        plt.xlabel('f (Hz)', color='green')
        #plt.ylim(0.0001, 100000)

    plt.ylabel('V', color='green')
    plt.grid(linestyle = 'dotted', color='green')

    fig.canvas.draw()
    plt.pause(0.1)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-l', '--list-devices', action='store_true',
              help='show list of audio devices and exit')
    parser.add_argument('-d', '--device', type=int, default=0,
              help='device index')
    parser.add_argument('-c', '--channels', type=int, default=1,
              help='number of channels to record')
    parser.add_argument('-s', '--samplerate', type=int, default=88200,
              help='number of samples per second')
    parser.add_argument('-n', '--samples', type=int, default=88200,
              help='number of samples to capture')
    parser.add_argument('-t', '--timeplot', action='store_true',
            help='plot a(t) instead of spectrum')
    parser.add_argument('-r', '--raw', action='store_true',
            help='print raw data')
    parser.add_argument('-m', '--rounds', type=int, default=1,
            help='number of cc rounds')

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    main(args)
