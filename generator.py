import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
import os
from scipy.fft import rfft, rfftfreq
THIS_FOLDER= os.path.dirname(os.path.abspath(__file__))

SAMPLE_RATE =20000   # Hertz
DURATION = 2  # Seconds
N = SAMPLE_RATE * DURATION      # Number of samples 

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)        # Generate a 2 hertz sine wave that lasts for 5 seconds
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

_,tone1 = generate_sine_wave(1000, SAMPLE_RATE, DURATION)
_,tone2 = generate_sine_wave(2000, SAMPLE_RATE, DURATION)
_,tone3 = generate_sine_wave(3000, SAMPLE_RATE, DURATION)
_,tone4 = generate_sine_wave(4000, SAMPLE_RATE, DURATION)
_,tone5 = generate_sine_wave(5000, SAMPLE_RATE, DURATION)
_,tone6 = generate_sine_wave(6000, SAMPLE_RATE, DURATION)
_,tone7 = generate_sine_wave(7000, SAMPLE_RATE, DURATION)
_,tone8 = generate_sine_wave(8000, SAMPLE_RATE, DURATION)
_,tone9 = generate_sine_wave(9000, SAMPLE_RATE, DURATION)
_,tone10 = generate_sine_wave(10000, SAMPLE_RATE, DURATION)

mixed_tone = tone1+ tone2+ tone3+ tone4+ tone5+ tone6+ tone7+ tone8+ tone9+ tone10

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

write(os.path.join(THIS_FOLDER,"test3.wav"), SAMPLE_RATE, normalized_tone)

yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / SAMPLE_RATE)
plt.plot(xf, np.abs(yf))
plt.show()


