#!/usr/bin/env python3

import time
import sounddevice as sd
import numpy as np
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt


mpl.rcParams['text.color'] = 'green'
mpl.rcParams['axes.labelcolor'] = 'green'
mpl.rcParams['xtick.color'] = 'green'
mpl.rcParams['ytick.color'] = 'green'

#Sis 2i2: 44.1kHz, 48kHz, 88.2kHz, 96kHz, 176.4kHz, 192kHz
rates = [44100, 48000, 88200, 96000, 176400, 192000]

sd.default.samplerate = 88200
#sd.default.dtype = 'int32'
sd.default.channels = 1


device_info = sd.query_devices(3, 'input')
print(device_info)

sf = 88200
dt = 0.1 # seconds
nsamples = int(sf * dt)


fig = plt.figure(figsize = (12, 6))
fig.patch.set_facecolor('black')

wind = np.hamming(nsamples)

while True:
    t = np.arange(nsamples)/sf
    rec = sd.rec(nsamples, samplerate=sf)
    sd.wait()

    ax = plt.subplot(111)
    ax.set_facecolor("black")
    ax.set_title(f'sample freq {sf} (Hz)', color='green')

    for axis in ['top', 'bottom', 'left', 'right']:
        #ax.spines[axis].set_linewidth(2.5)  # change width
        ax.spines[axis].set_color('green')    # change color


    if 1:
        sp = np.fft.rfft(rec, axis=0)
    else:
        sign = np.array(rec)
        filtd = np.multiply(sign, wind)
        sp = np.fft.rfft(filtd)


    N = len(sp)
    n = np.arange(N)
    T = N/sf
    f = n/T/2

    sp = np.abs(sp)
    maxidx = np.argmax(sp)
    maxfreq = maxidx/T/2
    maxval = 20*np.log10(np.amax(sp))

    textstr = f'f {maxfreq:7.1f} Hz\na {maxval:3.1f} dB'

    props = dict(boxstyle='round', facecolor='black', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

    plt.plot(f, 20*sp, color='green')
    #plt.plot(t, rec)
    plt.xlabel('f (Hz)', color='green')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.ylabel('dB', color='green')
    plt.ylim(0.01, 100000)
    plt.xlim(0, 22000)
    plt.grid(linestyle = 'dotted', color='green')


    plt.show(False)
    #plt.draw()
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.01)
    plt.clf()
