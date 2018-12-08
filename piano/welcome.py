#!/usr/bin/env python
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math
import pygame
import globalname
from pygame.locals import*


def welcomeinit():
    screen = pygame.display.set_mode((320,240))
    WHITE = 255,255,255
    BLACK = 0,0,0    
    my_font = pygame.font.Font(None,30)
    my_welcome = ['Welcome to Virtual Piano']
    my_welcome_pos = [(160,120)]
    screen.fill(BLACK)
    for label in range(1):
        my_text = my_welcome[label]
        text_pos = my_welcome_pos[label]
        text_surface = my_font.render(my_text, True, WHITE)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface,rect)
    while True:
        try:
            time.sleep(0.2)  # Without sleep, no screen output!          
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    if ( y < 120 and y > 40):
                        if ( x < 200 and x > 120):
                            globalname.instructment_type = 1
                            return 1
                    if( y < 200 and y > 120):
                        if ( x < 200 and x > 120):
                            globalname.instructment_type = 1
                            return 2
                    
            #print (2 )
            pygame.display.flip()
            return 0 
        except Keyboardinterrupt:  
    	    GPIO.cleanup()         


