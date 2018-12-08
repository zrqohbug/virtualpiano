
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings


def speedx(array, factor):
	length = len(array)
    indice = np.round(np.arange(0, length, factor))
    indice = indice[indice < length].astype(int)
    return array[indice]