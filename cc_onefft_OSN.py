# Python example - Fourier transform using numpy.fft method

import numpy as np
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plotter

def dofft(datain):
    # Frequency domain representation
    FFT = np.fft.fft(datain)/len(datain)           # Normalize amplitude
    FFT = FFT[range(int(len(datain)/2))] # Exclude sampling frequency

    tpCount     = len(datain)
    values      = np.arange(int(tpCount/2))
    timePeriod  = tpCount/samplingFrequency
    frequencies = values/timePeriod
    return (frequencies, FFT)

# How many time points are needed i,e., Sampling Frequency
samplingFrequency=100;

# At what intervals time points are sampled
samplingInterval= 1.0/samplingFrequency;

print("Interval {}".format(samplingInterval))

# Begin and End time period of the signals
beginTime           = 0.0;
endTime             = 10.0;

Npoints = (endTime - beginTime)/samplingInterval

# Frequency of the signals
signal1Frequency     = 4;
signal2Frequency     = 7;

# Time points
time = np.arange(beginTime, endTime, samplingInterval);
noiseA = 20 * np.random.rand(len(time))
noiseB = 20 * np.random.rand(len(time))

# Create two sine waves
amplitude1 = np.sin(2*np.pi*signal1Frequency*time)
amplitude2 = np.sin(2*np.pi*signal2Frequency*time)

# Create subplot
figure, axis = plotter.subplots(3, 2)
plotter.subplots_adjust(hspace=1)

# Add the sine waves

C = amplitude1 + amplitude2
A = 5 * C + noiseA
B = 5 * C + noiseB
# Time domain representation of the resultant sine wave
pix = 0
axis[pix, 0].set_title('C(t)')
axis[pix, 0].plot(time, C)
axis[pix, 0].set_xlabel('Time')
axis[pix, 0].set_ylabel('Amplitude')

# Frequency domain representation
pix = 1
axis[pix, 0].set_title('A(t)')
axis[pix, 0].plot(time, A)
axis[pix, 0].set_xlabel('Time')
axis[pix, 0].set_ylabel('Amplitude')

pix = 1
axis[pix, 1].set_title('B(t)')
axis[pix, 1].plot(time, B)
axis[pix, 1].set_xlabel('Time')
axis[pix, 1].set_ylabel('Amplitude')

fa, fftresa = dofft(A)
fb, fftresb = dofft(B)

fftres = fftresa * np.conjugate(fftresb)

# Frequency domain representation
pix = 0
fftres = abs(fftres)
fftres[0] = 0.01
axis[pix, 1].set_title('CC spectrum')
axis[pix, 1].plot(fa, fftres)
axis[pix, 1].set_xlabel('Frequency')
axis[pix, 1].set_ylabel('Amplitude')
axis[pix, 1].set_yscale('log')


pix = 2
fftresa = abs(fftresa)
fftresa[0] = 0.01
axis[pix, 0].set_title('FFT(A)')
axis[pix, 0].plot(fa, fftresa)
axis[pix, 0].set_xlabel('Frequency')
axis[pix, 0].set_ylabel('Amplitude')
axis[pix, 0].set_yscale('log')

pix = 2
fftresb = abs(fftresb)
fftresb[0] = 0.01
axis[pix, 1].set_title('FFT(B)')
axis[pix, 1].plot(fb, fftresb)
axis[pix, 1].set_xlabel('Frequency')
axis[pix, 1].set_ylabel('Amplitude')
axis[pix, 1].set_yscale('log')



plotter.show()
