#!/usr/bin/env python

from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings
import stretch 
import speedx 


def shift_pitch(array, n, size=2**13, height=2**11):
    factor = 2**(1.0 * n / 12.0)
    stretch_result = stretch.stretch(array, 1.0/factor, size, height)
    return speedx.speedx(stretch_result[size:], factor)



