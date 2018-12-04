
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings


def parse_arguments():
    description = ('"virtual piano"')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--wav', '-w',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='bowl.wav',
        help='WAV file')
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='typetest.kb',
        help='keyboard file')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='verbose mode')

    return (parser.parse_args(), parser)
