#!/usr/bin/env python3

import argparse
import sounddevice as sd
from collections import namedtuple

input = namedtuple('input', ['device', 'samplerate', 'samples', 'channels', 'norm'])

def main(input, rounds):
    sd.default.device = input.device
    sd.default.channels = input.channels
    sd.default.samplerate = input.samplerate

    device_info = sd.query_devices(input.device, 'input')
    print(f'Recording from {device_info["name"]}')
    print(f'collect {input.samples} samples ({input.samples/input.samplerate:.2f} s)')

    maxs = [0 for _ in range(input.channels)]
    mins = [0 for _ in range(input.channels)]

    n = 0
    for r in range(rounds):
        print(f'round {r}')
        rec = sd.rec(input.samples)
        sd.wait()
        n += 1

        for ch in range(input.channels):
            print(f'  channel {ch}')
            data = [x[ch] for x in rec]
            maxVal = max(data)
            minVal = min(data)

            print(f'    max: {maxVal:.9f}, min: {minVal:.9f}')
            maxs[ch] += maxVal
            mins[ch] += minVal
            print(f'    avg: {maxs[ch]/n:.9f}, avg: {mins[ch]/n:.9f}')

    for ch in range(input.channels):
        print(f'ch {ch} - calibration ({input.norm} V) {input.norm/maxs[ch]:.5f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument('--device', type=str, default='Scarlett',
        help='device index/name')
    parser.add_argument('--channels', type=int, default=2,
        help='number of channels to record (1 or 2)')
    parser.add_argument('--srate', type=int, default=192000,
        help='number of samples per second')
    parser.add_argument('--samples', type=int, default=192000,
        help='number of samples to capture')
    parser.add_argument('--norm', type=float, default=1.0,
        help='normalization (to 1V)')
    parser.add_argument('--rounds', type=int, default=1,
        help='averaging rounds')

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    assert args.srate == args.samples
    assert args.channels == 1 or args.channels == 2, "invalid number of channels"

    input = input(args.device, args.srate, args.samples, args.channels, args.norm)

    main(input, args.rounds)
