#!/usr/bin/env python

from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings
import parse_arguments 
import stretch 
import pitchshift 
import speedx 
import welcome
import display
import time


def main():
    os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
    # Parse command line arguments
    (args, parser) = parse_arguments.parse_arguments()

    # Enable warnings from scipy if requested
    if not args.verbose:
        warnings.simplefilter('ignore')

    fps, sound = wavfile.read(args.wav.name)

    tones = range(-24, -12)
    sys.stdout.write('Transponding sound file... ')
    sys.stdout.flush()
    transposed_sounds = [pitchshift.pitchshift(sound, n) for n in tones]
    print('DONE')

    # So flexible ;)
    pygame.mixer.init(fps, -16, 1, 2048)
    # For the focus
    screen = pygame.display.set_mode((320,240))

    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
    playing = {k: 0 for k in keys}
    note_duration = 0
    note_length = 0
    tune_length = 0

    while (welcome.welcomeinit() == 0):
        print ('Virtual Piano')

    while True:
        event = pygame.event.wait()
        screen.fill(BLACK)
        display.display()
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (playing[key] == 0):
                key_sound[key].play(fade_ms=50)
                playing[key] = 1
                a = time.time()

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # Stops with 50ms fadeout
            key_sound[key].fadeout(50)
            playing[key] = 0
            b = time.time()

        note_duration = b - a
        display.displaynote()
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')
