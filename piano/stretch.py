
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings


def stretch(array, fac, window_size, h):
    """ Stretches/shortens a sound, by some fac """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(array) / fac + window_size))

    for i in np.arange(0, len(array) - (window_size + h), h*fac):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = array[i: i + window_size]
        a2 = array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/fac)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')


