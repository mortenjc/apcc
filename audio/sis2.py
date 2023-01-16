#!/usr/bin/env python3

import time, argparse, sys
import sounddevice as sd
import numpy as np
import matplotlib as mpl
#mpl.use('tkagg')
import matplotlib.pyplot as plt

def main(device, samplerate, nsamples):
    mpl.rcParams['text.color'] = 'green'
    mpl.rcParams['axes.labelcolor'] = 'green'
    mpl.rcParams['xtick.color'] = 'green'
    mpl.rcParams['ytick.color'] = 'green'

    sd.default.channels = 1
    sd.default.samplerate = samplerate

    device_info = sd.query_devices(device, 'input')
    print(device_info)

    sf = samplerate
    print(f'collect {nsamples} samples ({nsamples/samplerate:.2f} s)')

    fig = plt.figure(figsize = (12, 6))
    fig.patch.set_facecolor('black')
    plt.ion()
    plt.show()

    wind = np.hamming(nsamples)

    while True:
        t = np.arange(nsamples)/sf
        rec = sd.rec(nsamples, samplerate=sf)
        sd.wait()

        ax = plt.subplot(111)

        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_color('green')    # change color

        ax.set_facecolor("black")
        ax.set_title(f'sample freq {sf} (Hz)', color='green')
        ax.set_facecolor("black")

        if 1:
            sp = np.fft.rfft(rec, axis=0)
        else:
            sp = np.fft.rfft(np.multiply(rec, wind), axis=0)

        N = len(sp)
        n = np.arange(N)
        T = N/sf
        f = n/T/2

        sp = np.abs(sp)
        # maxidx = np.argmax(sp)
        # maxfreq = maxidx/T/2
        # maxval = np.amax(sp)
        #
        # textstr = f'f {maxfreq:7.1f} Hz\na {maxval:3.1f} dB'
        #
        # props = dict(boxstyle='round', facecolor='black', alpha=0.5)
        # ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        #     verticalalignment='top', bbox=props)

        plt.plot(f, sp, color='green')

        plt.xlabel('f (Hz)', color='green')
        #ax.set_xscale('log')
        ax.set_yscale('log')
        plt.ylabel('a.u.', color='green')
        plt.ylim(0.01, 100000)
        plt.xlim(0.01, 22000)
        plt.grid(linestyle = 'dotted', color='green')

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01)
        plt.clf()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
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

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    main(args.device, args.samplerate, args.samples)
