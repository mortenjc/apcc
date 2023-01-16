import numpy
import soundcard as sc

# get a list of all speakers:
#speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()
# get a list of all microphones:
mics = sc.all_microphones()
# get the current default microphone on your system:
default_mic = sc.default_microphone()

# search for a sound card by substring:
#>>> sc.get_speaker('Scarlett')
#<Speaker Focusrite Scarlett 2i2 (2 channels)>
#>>> one_mic = sc.get_microphone('Scarlett')
#<Microphone Focusrite Scalett 2i2 (2 channels)>
# fuzzy-search to get the same results:
one_speaker = sc.get_speaker('FS2i2')
one_mic = sc.get_microphone('FS2i2')

print(default_speaker)
#<Speaker Focusrite Scarlett 2i2 (2 channels)>
print(default_mic)
#<Microphone Focusrite Scarlett 2i2 (2 channels)>

# record and play back one second of audio:
data = default_mic.record(samplerate=48000, numframes=48000)
default_speaker.play(data/numpy.max(data), samplerate=48000)

# alternatively, get a `Recorder` and `Player` object
# and play or record continuously:
# with default_mic.recorder(samplerate=48000) as mic, \
#       default_speaker.player(samplerate=48000) as sp:
#     for _ in range(100):
#         data = mic.record(numframes=1024)
#         sp.play(data)
