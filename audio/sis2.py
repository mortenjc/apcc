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



def plot_setup(interactive=False):
    #plt.ion()

    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor("black")
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_color('green')

    return fig, ax


def main(args):
    device = args.device
    samplerate = args.srate
    nsamples = args.samples
    channels = args.channels
    norm = args.norm

    fig, ax = plot_setup()

    sd.default.device = device
    sd.default.channels = channels
    sd.default.samplerate = samplerate

    assert samplerate == 192000
    assert nsamples == 192000
    assert channels == 1 or channels == 2, "invalid number of channels"


    device_info = sd.query_devices(device, 'input')
    print(device_info)

    sf = samplerate
    print(f'collect {nsamples} samples ({nsamples/samplerate:.2f} s)')

    #wind = np.hamming(nsamples)

    while True:
        rec = sd.rec(nsamples)
        sd.wait()

        t = np.arange(nsamples)/sf
        c1 = [x[0] for x in rec]
        sp1 = np.fft.rfft(c1, norm='ortho')

        if channels == 2:
            c2 = [x[1]/0.04 for x in rec]
            sp2 = np.fft.rfft(c2, norm='ortho')


        N = len(sp1)
        n = np.arange(N)
        T = N/sf
        f = n/T/2

        # sp = np.abs(sp)
        # maxidx = np.argmax(sp)
        # maxfreq = maxidx/T/2
        # maxval = np.amax(sp)

        # textstr = f'f {maxfreq:7.1f} Hz\nampl {maxval:3.1f}'
        #
        # props = dict(boxstyle='round', facecolor='black', alpha=0.5)
        # ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        #     verticalalignment='top', bbox=props)


        ax.clear()
        ax.set_title(f'sample freq {sf} (Hz)', color='green')

        if args.timeplot:
            plt.plot(t, c1, color='green')
            if channels == 2:
                plt.plot(t, c2, color='blue')
            plt.xlabel('t (s)', color='green')
            plt.xlim(0.0, 1.0)
        else:
            plt.plot(f, np.abs(sp1)/norm, color='green')
            if channels == 2:
                plt.plot(f, np.abs(sp2)/norm, color='blue')
            plt.xlim(1.0, 22000)
            ax.set_xscale('log')
            ax.set_yscale('log')
            plt.xlabel('f (Hz)', color='green')
            #plt.ylim(0.0001, 100000)

        plt.ylabel('V', color='green')
        plt.grid(linestyle = 'dotted', color='green')


        fig.canvas.draw()
        plt.pause(0.1)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')

    parser.add_argument('--device', type=int, default=0,
        help='device index')

    parser.add_argument('--channels', type=int, default=1,
        help='number of channels to record')

    parser.add_argument('--srate', type=int, default=88200,
        help='number of samples per second')

    parser.add_argument('--samples', type=int, default=88200,
        help='number of samples to capture')

    parser.add_argument('--norm', type=float, default=1.0,
        help='normalization (to 1V)')

    parser.add_argument('-t', '--timeplot', action='store_true',
        help='plot a(t) instead of spectrum')

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    main(args)
