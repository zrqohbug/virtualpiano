
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
        default='bowl.wav'
        )
    '''parser.add_argument(
        '--piano', '-p',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='piano.wav'
        )'''
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='typetest.kb'
        )
    parser.add_argument(
        '--keyall', '-kal',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='typeall.kb'
        )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true'
        )

    return (parser.parse_args(), parser)

