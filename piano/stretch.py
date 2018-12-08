
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys


def stretch(array, factor, size, height):
    length = len(array)
    result_length = int( length / factor + size)
    result = np.zeros(result_length)
    phase = np.zeros(size)
    hanning = np.hanning(size)

    for i in np.arange(0, length - (size + height), height * factor):
        i = int(i)
        p1 = array[i: i + size]
        p2 = array[i + height: i + size + height]

        s1 = np.fft.fft(hanning * p1)
        s2 = np.fft.fft(hanning * p2)

        phase = (phase + np.angle(s2/s1)) % 2 * np.pi

        p2_rephased = np.fft.ifft(np.abs(s2) * np.exp(1j * phase))
        i_v = int(i/factor)
        result[i_v: i_v + size] += hanning * p2_rephased.real

    result = (4096 * result/result.max())

    return result.astype('int16')


