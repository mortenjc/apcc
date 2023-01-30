#!/usr/bin/env python3

# Copyright (C) 2023 Morten Jagd Christensen
# scard() is a wrapper for the sounddevice package

import sounddevice as sd
import numpy as np
from collections import namedtuple


input = namedtuple('input', ['device', 'samplerate', 'samples', 'channels', 'norm'])

def query_devices():
    print(sd.query_devices())

class scard():
    def __init__(self, input):
        print(input)
        self.input = input
        sd.default.device = input.device
        sd.default.channels = input.channels
        sd.default.samplerate = input.samplerate


    def record(self, norm):
        nchan = self.input.channels
        nsamp =self.input.samples
        rec = sd.rec(nsamp)
        sd.wait()
        res = [[] for _ in range(nchan)]
        for ch in range(nchan):
            res[ch] = [norm * x[ch] for x in rec]

        assert len(res) == nchan, 'recording error (# of channels)'
        assert len(res[0]) == nsamp, 'recording error (# of samples)'
        return res


    def query(self):
        return sd.query_devices(self.input.device, 'input')


    def stat(self, data):
        nchan = self.input.channels
        maxs = [0 for _ in range(nchan)]
        mins = [0 for _ in range(nchan)]

        for ch in range(nchan):
            maxs[ch] = np.max(data)
            mins[ch] = np.min(data)

        return mins, maxs
