#!/usr/bin/env python

from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings
import stretch 
import speedx 


def shift_pitch(array, n, window_size=2**13, h=2**11):
    fac = 2**(1.0 * n / 12.0)
    stretch_result = stretch.stretch(array, 1.0/fac, window_size, h)
    return speedx.speedx(stretch_result[window_size:], fac)



