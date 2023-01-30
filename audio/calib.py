#!/usr/bin/env python3

#

import argparse, scard

def main(scard, rounds):

    device_info = scard.query()
    print(f'Recording from {device_info["name"]}')
    print(f'collect {input.samples} samples ({input.samples/input.samplerate:.2f} s)')

    maxs = [0 for _ in range(input.channels)]
    mins = [0 for _ in range(input.channels)]

    n = 0
    for r in range(rounds):
        print(f'round {r}')
        rec = scard.record(1.0)
        n += 1

        tmin, tmax = scard.stat(rec)
        print(tmin)
        for ch in range(input.channels):
            print(f'    max: {tmax[ch]:.9f}, min: {tmin[ch]:.9f}')
            maxs[ch] += tmax[ch]
            mins[ch] += tmin[ch]
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
        help='normalization (to [norm] V)')
    parser.add_argument('--rounds', type=int, default=1,
        help='averaging rounds')

    args, remaining = parser.parse_known_args()

    #assert args.srate == args.samples
    #assert args.channels == 1 or args.channels == 2, "invalid number of channels"

    if args.list_devices:
        scard.query_devices()
        parser.exit(0)

    input = scard.input(args.device, args.srate, args.samples, args.channels, args.norm)
    scard = scard.scard(input)

    main(scard, args.rounds)
