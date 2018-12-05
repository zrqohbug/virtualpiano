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
import shift_pitch
import speedx 
import welcome
import display
import time
import globalname
import GPIOinput
import volume
import socket
import time
import wifi

def main():
    
    '''os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')'''
    
    wifi.init()

    
    UDP_IP = "192.168.4.9"
    UDP_PORT = 9008

    MESSAGE = "Break!"

    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    print "message:", MESSAGE

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    #sock.sendto(MESSAGE, (UDP_IP,UDP_PORT))
    sock2.bind(("192.168.4.1",8080))
    
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

    # Enable warnings from scipy if requested
    if not args.verbose:
        warnings.simplefilter('ignore')

    fps, sound = wavfile.read(args.wav.name)

    tones = range(-24, -12)
    tones_all = range(-48, 12)
    sys.stdout.write('Ready for the computation.. ')
    sys.stdout.flush()
    transposed_sounds = [shift_pitch.shift_pitch(sound, n) for n in tones]
    #transposed_all = [shift_pitch.shift_pitch(sound, n) for n in tones_all]
    pygame.mixer.init(fps, -16, 1, 2048)
    # init############################################################################
    screen = pygame.display.set_mode((320,240))
    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
    playing = {k: 0 for k in keys}
    note_duration = {k: 0 for k in keys}
    former_duration = {k: 0 for k in keys}
    rest_duration = 0
    note_length = 0
    tune_length = 0
    pygame.init()
    pygame.mouse.set_visible(True)
    WHITE = 255,255,255
    BLACK = 0,0,0
    GPIO.setmode(GPIO.BCM)
    a = {k: 0 for k in keys}
    a_rest = 0
    b = {k: 0 for k in keys}
    b_rest = 0
    
    #a.append(0)
    #b.append(0)
    start = 0
    current_status = 0
    KEYDOWN = 99
    KEYUP = 100
    genrestflag = 0
    needtogenerate  = 0
    #################################################################################
    while (welcome.welcomeinit() == 0):
        a = {k: time.time() for k in keys}
        b = {k: time.time() for k in keys}
        a_rest = time.time()
        b_rest = time.time()
        #print(1)
        #print ('Virtual Piano')
    screen.fill(WHITE)
    display.displaykey(screen)
    #print (a,b,keys)
    while True:
        #event = pygame.event.poll()
        #print (n)          
            
        #else:
            #print "receive data:", data
            
        key = str(globalname.n[1])
        event = globalname.n[0]
        #print (key,event)
        pygame.display.flip()
        '''if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)'''
    

        '''if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (playing[key] == 0):
                key_sound[key].play(fade_ms=50)
                playing[key] = 1
                b = time.time()
                note_duration = b - a
                a = time.time()
                current_status = 1
                #print (note_duration)'''
        if event == KEYDOWN:
            #print (globalname.n)
            if (key in key_sound.keys()) and (playing[key] == 0):
                #sock.sendto(MESSAGE, (UDP_IP,UDP_PORT))
                #data, addr = sock2.recvfrom(10)
                #print "receive data:", data
                
                '''if data == 'L':
                    print "-------------------------------------receive button L"
                    globalname.location -= 1
                    
                elif data == 'R':
                    print "-------------------------------------receive button R"
                    globalname.location += 1 
            
                elif data == 'F':
                    print "-------------------------------------receive button F"'''
                
                
                key_sound[key].play(fade_ms=50)
                playing[key] = 1
                b_rest = time.time()
                rest_duration = b_rest - a_rest
                a[key] = time.time()
                current_status = 1
                needtogenerate = 1
                if (needtogenrest == 0):
                    genrestflag = 1
                needtogenrest = 0

                #print (note_duration)
                
                '''time.sleep(0.01)
                data, addr = sock2.recvfrom(10)
                print "receive data:", data
                time.sleep(0.01)
                data, addr = sock2.recvfrom(10)
                print "receive data:", data
                time.sleep(0.01)
                data, addr = sock2.recvfrom(10)
                print "receive data:", data
                time.sleep(0.01)
                data, addr = sock2.recvfrom(10)
                print "receive data:", data
                time.sleep(0.01)
                data, addr = sock2.recvfrom(10)
                print "receive data:", data'''


            '''elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt'''

        elif event == KEYUP and key in key_sound.keys():
            print (globalname.n)
            # Stops with 50ms fadeout
            key_sound[key].fadeout(50)
            playing[key] = 0

            b[key] = time.time()
            note_duration[key] = b[key] - a[key]
            needtogenerate = 0
            if '1' in playing.value():
                pass
            else:
                a_rest = time.time()
                needtogenrest = 1
            #print (note_duration)
            start = 1
            globalname.n[0] = 0
            
        for keyv in key_sound.keys():  
            if ( former_duration[keyv] != note_duration[keyv] ):
                if (needtogenerate == 0):
                    display.appendnote(key,note_duration[keyv],keys)
            former_duration[keyv] = note_duration[keyv]

        if (start and needtogenrest == 0 and genrestflag == 0):
            display.appendrest(rest_duration)
        genrestflag = 0    
        #print(note_duration)
        screen.fill(WHITE)
        if (current_status == 0):
            display.displaykey(screen)
        else:
            display.displaykeyboard(key,keys,screen)            
        display.displaybase(screen)
        if (start) :
            display.displaynote(screen)
        #display.display(notelist)
        
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Thank you for playing')
