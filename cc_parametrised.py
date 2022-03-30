# Python example - Fourier transform using numpy.fft method

import numpy as np
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plotter
import argparse


#
def noise(len, noiseamp):
    return noiseamp * (np.random.rand(len) - 0.5)


# Do FFT analysis
def dofft(datain, fs):
    FFT = np.fft.fft(datain)/len(datain) # Normalize amplitude
    FFT = FFT[range(int(len(datain)/2))] # Exclude sampling frequency

    tpCount     = len(datain)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/fs
    freqs = values/timePeriod
    return (freqs, FFT)


# Do multi-round conjugate correlation
def ccmrounds(C, fs, rounds, noiseampl, crossnoise):
    # Initial step to get a zero filled array of correct size
    f, cc = dofft(C, fs)
    cc = cc * 0

    for i in range(rounds):
        common = noise(len(C), crossnoise)
        A = C + noise(len(C), noiseampl) + common
        B = C + noise(len(C), noiseampl) + common

        fa, fftresa = dofft(A, fs)
        fb, fftresb = dofft(B, fs)

        fftres = fftresa * np.conjugate(fftresb)
        cc = cc + fftres
    return f, cc


def plotfft(ax, f, fftres, rounds):
    ax.set_title('CC spectrum (m={})'.format(rounds))
    ax.plot(f, 10*np.log10(fftres))
    ax.set_xlabel('f')
    ax.set_ylabel('dB')
    #ax.set_yscale('log')


def plottime(ax, t, C, title):
    ax.set_title(title)
    ax.plot(t, C)
    ax.set_xlabel('t')
    ax.set_ylabel('ampl.')


def mrounds(rounds, noiseampl, crossnoise):
    samplingFrequency = 100
    samplingInterval= 1.0/samplingFrequency

    # Begin and End time period of the signals
    beginTime = 0.0
    endTime = 10.0

    # Frequency of the two sine waves
    f1 = 4
    f2 = 7
    # Time points
    time = np.arange(beginTime, endTime, samplingInterval);

    # Create two sine waves
    amplitude1 = np.sin(2*np.pi * f1 * time)
    amplitude2 = np.sin(2*np.pi * f2 * time)
    C = amplitude1 + amplitude2

    # Example of time representation of A(t)
    noiseA = noise(len(time), noiseampl) + noise(len(time), crossnoise)

    # Create subplot
    figure, axis = plotter.subplots(3, 1)
    plotter.subplots_adjust(hspace=1)

    # Time domain representation of the resultant sine wave
    plottime(axis[0], time, C, 'C(t)')

    # one example of the noisy signal
    A = C + noiseA
    plottime(axis[1], time, A, 'A(t) example')

    #
    f, cc = ccmrounds(C, samplingFrequency, rounds, noiseampl, crossnoise)
    plotfft(axis[2], f, np.sqrt(abs(cc))/rounds, rounds)
    plotter.show()


#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CC processing')
    parser.add_argument('--rounds', '-r', help='rounds', type=int, default=1)
    parser.add_argument('--noiseampl', '-na', help='noise (uncorrelated)', type=int, default=0)
    parser.add_argument('--corrnoise', '-nc', help='noise (common)', type=int, default=0)
    args = parser.parse_args()

    mrounds(args.rounds, args.noiseampl, args.corrnoise)
