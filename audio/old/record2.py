#!/usr/bin/env python3

import argparse, sys, time, queue
import numpy as np
import sounddevice as sd
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plotter


def plottime(f, r, n):
    figure, ax = plotter.subplots(1, 1)
    plotter.subplots_adjust(hspace=1)
    assert len(f) == n

    #ax.set_title(title)
    t = np.arange(len(f))
    ax.plot(t, f)
    ax.set_xlabel('t')
    ax.set_ylabel('ampl.')

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-l', '--list-devices', action='store_true',
          help='show list of audio devices and exit')
parser.add_argument('-d', '--device', type=int, default=0,
          help='device index')
parser.add_argument('-c', '--channels', type=int, default=1,
          help='number of channels to record')
parser.add_argument('-s', '--samplerate', type=int, default=0,
          help='number of samples per second')
parser.add_argument('-n', '--samples', type=int, default=1024,
          help='number of samples to capture')

args, remaining = parser.parse_known_args()

if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)

q = queue.Queue()

received = 0
def audio_callback(indata, frames, time, status):
    global received
    global data
    """This is called (from a separate thread) for each audio block."""
    received = received + len(indata)
    q.put(indata)


try:
    adevice = args.device
    device_info = sd.query_devices(adevice, 'input')
    print(device_info)
    if args.samplerate == 0:
        asamplerate = device_info['default_samplerate']
    else:
        asamplerate = args.samplerate
    print("sample rate supported {}, selected {}".format(
           device_info['default_samplerate'], asamplerate))

    stream = sd.InputStream(device=adevice, channels=args.channels,
        samplerate=asamplerate, callback=audio_callback)

    with stream:
        while True:
            if received >= args.samples:
                print("received {} sampels".format(received))
                break

    print("length {}".format(q.qsize()))

    ref = np.arange(0)
    for i in range(q.qsize()):
        data = q.get()
        ref = np.append(ref, data[:,0])
    print(f'len(ref) {len(ref)}')
    assert len(ref) == args.samples
    print(f'samplerate {asamplerate} ')
    print(f' ampl max {np.amax(ref)}')
    print(f' ampl min {np.amin(ref)}')
    plottime(ref, asamplerate)
    plotter.show()



except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
