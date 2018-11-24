#!/usr/bin/env python

from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import sys
import warnings
import RPi.GPIO as GPIO
import time
import subprocess
import math

import parse_arguments 
import stretch 
import pitchshift 
import speedx 
import welcome
import display
import time
import globalname


def main():
    '''os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')'''
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
    # init############################################################################
    screen = pygame.display.set_mode((320,240))
    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
    playing = {k: 0 for k in keys}
    note_duration = 0
    former_duration = 0
    note_length = 0
    tune_length = 0
    pygame.init()
    pygame.mouse.set_visible(True)
    WHITE = 255,255,255
    BLACK = 0,0,0
    GPIO.setmode(GPIO.BCM)
    a = 0
    b = 0
    current_status = 0
    #################################################################################
    while (welcome.welcomeinit() == 0):
        a = time.time()
        b = time.time()
        print ('Virtual Piano')
    screen.fill(WHITE)
    while True:
        event = pygame.event.poll()

        pygame.display.flip()
        #display.display()
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (playing[key] == 0):
                key_sound[key].play(fade_ms=50)
                playing[key] = 1
                b = time.time()
                note_duration = b - a
                a = time.time()
                current_status = 1
                print (note_duration)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # Stops with 50ms fadeout
            key_sound[key].fadeout(50)
            playing[key] = 0
            b = time.time()
            note_duration = b - a
            a = time.time()
            current_status = 0
            print (note_duration)
            
        if ( former_duration != note_duration ):
            if (current_status == 0):
                display.appendnote(key,note_duration,keys)
            else:
                display.appendrest(note_duration)
        #print(note_duration)
        display.displaybase(screen)
        #display.display(notelist)
        former_duration = note_duration
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Thank you for playing')
