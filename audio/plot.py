#!/usr/bin/env python3


import matplotlib as mpl
mpl.use('macosx')
import matplotlib.pyplot as plt


class plot():
    def __init__(self):
        mpl.rcParams['text.color'] = 'green'
        mpl.rcParams['axes.labelcolor'] = 'green'
        mpl.rcParams['xtick.color'] = 'green'
        mpl.rcParams['ytick.color'] = 'green'

        fig, ax = plt.subplots(1)
        fig.patch.set_facecolor('black')
        ax.set_facecolor("black")
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_color('green')

        self.fig = fig
        self.ax = ax

        self.colors = ['green', 'blue']


    def plotamp(self, t, amp, title):
        # textstr = f'f {maxfreq:7.1f} Hz\nampl {maxval:3.1f}'
        #
        # props = dict(boxstyle='round', facecolor='black', alpha=0.5)
        # ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        #     verticalalignment='top', bbox=props)

        self.ax.set_title(title, color='green')
        plt.xlabel('t (s)', color='green')
        plt.ylabel('V', color='green')
        plt.xlim(0.0, 1.0)

        for ds in range(len(amp)):
            plt.plot(t, amp[ds], color=self.colors[ds])

        plt.grid(linestyle = 'dotted', color='green')

        self.fig.canvas.draw()
        plt.pause(0.1)
        plt.show()


    def plotfft(self, f, spec):
        plt.xlabel('f (Hz)', color='green')
        plt.ylabel('a.u.', color='green')
        plt.xlim(1.0, 22000)
        #plt.ylim(0.0001, 100000)
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')

        for ds in range(len(spec)):
            print(f'adding data {ds}')
            plt.plot(f, spec[ds], color=self.colors[ds])

        plt.grid(linestyle = 'dotted', color='green')

        self.fig.canvas.draw()
        plt.pause(0.1)
        plt.show()
