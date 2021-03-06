#!/usr/bin/env python
import os
from scipy.io import wavfile
import argparse
import numpy as np
import pygame
from pygame.locals import*
import sys
import warnings
import RPi.GPIO as GPIO
import time
import subprocess
import math
import threading
import socket

import parse_arguments 
import stretch 
import shift_pitch
import speedx 
import welcome
import display
import time
import globalname
import GPIOinput
import volume
import wifi



def main():
    
    # PiTFT init#################
    os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')


    # Wifi port init#################
    wifi.init()
    UDP_IP = "192.168.4.9"
    UDP_PORT = 9008

    MESSAGE = "w"

    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    print "message:", MESSAGE
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(("192.168.4.1",8080))

    # GPIO init#################

    volume.volumechange(100)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(5,GPIO.BOTH,callback=GPIOinput.GPIO5_both)
    GPIO.add_event_detect(6,GPIO.BOTH,callback=GPIOinput.GPIO6_both)
    GPIO.add_event_detect(12,GPIO.BOTH,callback=GPIOinput.GPIO12_both)
    GPIO.add_event_detect(13,GPIO.BOTH,callback=GPIOinput.GPIO13_both)
    GPIO.add_event_detect(16,GPIO.BOTH,callback=GPIOinput.GPIO16_both)
    GPIO.add_event_detect(17,GPIO.BOTH,callback=GPIOinput.GPIO17_both)
    GPIO.add_event_detect(18,GPIO.BOTH,callback=GPIOinput.GPIO18_both)
    GPIO.add_event_detect(19,GPIO.BOTH,callback=GPIOinput.GPIO19_both)
    GPIO.add_event_detect(20,GPIO.BOTH,callback=GPIOinput.GPIO20_both)
    GPIO.add_event_detect(21,GPIO.BOTH,callback=GPIOinput.GPIO21_both)
    GPIO.add_event_detect(22,GPIO.BOTH,callback=GPIOinput.GPIO22_both)
    GPIO.add_event_detect(23,GPIO.BOTH,callback=GPIOinput.GPIO23_both)
    GPIO.add_event_detect(26,GPIO.BOTH,callback=GPIOinput.GPIO26_both)
    GPIO.add_event_detect(27,GPIO.BOTH,callback=GPIOinput.GPIO27_both) 
    
    # Parse command line arguments
    (args, parser) = parse_arguments.parse_arguments()
    if not args.verbose:
        warnings.simplefilter('ignore')

    # Generate sound #################
    fps, sound = wavfile.read(piano.wav)
    tones = range(-24, -12)
    tones_all = range(-48, 12)
    sys.stdout.write('Ready for the computation.. ')
    sys.stdout.flush()
    transposed_sounds = [shift_pitch.shift_pitch(sound, n) for n in tones]
    
    pygame.mixer.init(fps, -16, 1, 2048)
    
    # Pygame display init############################################################################
    screen = pygame.display.set_mode((320,240))
    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
       
    keys_all = args.keyall.read().split('\n')
    transposed_sounds_all = [shift_pitch.shift_pitch(sound, n) for n in tones_all]
    sounds_all = map(pygame.sndarray.make_sound, transposed_sounds_all)
    key_sound_all = dict(zip(keys_all, sounds_all))
    
    print(keys)
    playing = {k: 0 for k in keys}
    note_duration = 0
    former_duration = 0
    rest_duration = 0
    note_length = 0
    tune_length = 0
    pygame.init()
    pygame.mouse.set_visible(False)
    WHITE = 255,255,255
    BLACK = 0,0,0
    GPIO.setmode(GPIO.BCM)
    a = 0
    a_rest = 0
    b = 0
    b_rest = 0    
    start = 0
    current_status = 0
    KEYDOWN = 99
    KEYUP = 100
    genrestflag = 0
    needtogenerate  = 1
    needtogenrest = 1
    

    # Program starts here################
    
    while (welcome.welcomeinit() == 0):
	    a = time.time()
	    b = time.time()
        #print(1)
        #print ('Virtual Piano')
    screen.fill(WHITE)
    display.displaykey(screen)
    #timer = threading.Timer(1,listenbutton)
    #timer.start()
    #print (a,b,keys)

    # main loop ################
    while True:            
        key = str(globalname.n[1])
        event = globalname.n[0]
        pygame.display.flip()
        # detect virtual button press ################
        if event == KEYDOWN:
            if (key in key_sound.keys()) and (playing[key] == 0):

            	# Use UDP signal to change volume ################
                sock.sendto(MESSAGE, (UDP_IP,UDP_PORT))
                data, addr = sock.recvfrom(100)
                globalname.mainlocation = int(data) % 10 - 2
                if (globalname.mainlocation == 3):
                    pygame.quit()
                vol = int(data) / 10
                if vol > 100:
                    sound_vol = 100
                elif vol > 40:
                	sound_vol = 90
                elif vol > 20:
                    sound_vol = 80
                else:
                	sound_vol = 70
                volume.volumechange(sound_vol)

                # generate note sound ################
                if (globalname.mainlocation >= 0):
                    sear = (globalname.mainlocation*100 + int(key) )
                else:
                    sear = (globalname.mainlocation*100 - int(key) )
                key_sound_all[str(sear)].play(fade_ms=50)
                playing[key] = 1

                # calculate rest duration ################                
                b = time.time()
                note_duration = b - a
                a = time.time()           
                current_status = 1

        # detect virtual button release ################
        elif event == KEYUP and key in key_sound.keys():

        	# generate note fade out ################
            if (globalname.mainlocation >= 0):
                sear = (globalname.mainlocation*100 + int(key) )
            else:
                sear = (globalname.mainlocation*100 - int(key) )
            key_sound_all[str(sear)].fadeout(50)

            # calculate note duration ################    
            playing[key] = 0
            b = time.time()
            note_duration = b - a
            a = time.time()
            start = 1
            globalname.n[0] = 0
            current_status = 0

        # append a note/rest to the note list ################    
        if ( former_duration != note_duration ):
            if (current_status == 0):
                display.appendnote(key,note_duration,keys)
            else:
                display.appendrest(note_duration)

        # display all things ################    
        screen.fill(WHITE)
        if (current_status == 0):
            display.displaykey(screen)
        else:
            display.displaykeyboard(key,keys,screen)            
        display.displaybase(screen)
        if (start) :
            display.displaynote(screen)
        former_duration = note_duration
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Thank you for playing')
