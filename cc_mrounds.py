# Python example - Fourier transform using numpy.fft method

import numpy as np
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plotter


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
def ccmrounds(C, fs, rounds, noiseampl):
    # Initial step to get a zero filled array of correct size
    f, cc = dofft(C, fs)
    cc = cc * 0

    for i in range(rounds):
        #common = noise(len(C), noiseampl/2)
        noiseA = noise(len(C), noiseampl)
        noiseB = noise(len(C), noiseampl)
        A = C + noiseA #+ common
        B = C + noiseB #+ common
        fa, fftresa = dofft(A, fs)
        fb, fftresb = dofft(B, fs)

        fftres = fftresa * np.conjugate(fftresb)
        cc = cc + fftres
    return f, cc


def plotfft(ax, f, fftres, rounds):
    ax.set_title('CC spectrum (m={})'.format(rounds))
    ax.plot(f, 10*np.log10(fftres))
    ax.set_xlabel('f')
    ax.set_ylabel('db')
    #ax.set_yscale('log')


def mrounds():
    samplingFrequency = 100
    noiseampl = 50

    # At what intervals time points are sampled
    samplingInterval= 1.0/samplingFrequency

    # Begin and End time period of the signals
    beginTime = 0.0
    endTime = 10.0

    Npoints = (endTime - beginTime)/samplingInterval

    # Frequency of the two sine waves
    f1 = 4
    f2 = 7
    # Time points
    time = np.arange(beginTime, endTime, samplingInterval);

    # Create two sine waves
    amplitude1 = np.sin(2*np.pi * f1 * time)
    amplitude2 = np.sin(2*np.pi * f2 * time)
    C = amplitude1 + amplitude2

    # Create subplot
    figure, axis = plotter.subplots(3, 2)
    plotter.subplots_adjust(hspace=1)

    # Add the sine waves
    noiseA = noise(len(time), noiseampl)
    noiseB = noise(len(time), noiseampl)


    # Time domain representation of the resultant sine wave
    ax = axis[0, 0]
    ax.set_title('C(t)')
    ax.plot(time, C)
    ax.set_xlabel('t')
    ax.set_ylabel('ampl.')

    # one example of the noisy signal
    A = C + noiseA
    ax = axis[1, 0]
    ax.set_title('A(t) example')
    ax.plot(time, A)
    ax.set_xlabel('t')
    ax.set_ylabel('ampl.')
    #
    rounds = 1
    f, cc = ccmrounds(C, samplingFrequency, rounds, noiseampl)
    plotfft(axis[2,0], f, abs(cc)/rounds, rounds)

    #
    rounds = 10
    f, cc = ccmrounds(C, samplingFrequency, rounds, noiseampl)
    plotfft(axis[0,1], f, abs(cc)/rounds, rounds)

    rounds = 100
    f, cc = ccmrounds(C, samplingFrequency, rounds, noiseampl)
    plotfft(axis[1,1], f, abs(cc)/rounds, rounds)

    rounds = 1000
    f, cc = ccmrounds(C, samplingFrequency, rounds, noiseampl)
    plotfft(axis[2,1], f, abs(cc)/rounds, rounds)

    plotter.show()


#
#
if __name__ == "__main__":
    print("Main called")
    mrounds()
