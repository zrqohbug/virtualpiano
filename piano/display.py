#!/usr/bin/env python
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math
import pygame
from pygame.locals import* 
    os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

def displaynote():
    pygame.mouse.set_visible(False)
    WHITE = 255,255,255
    BLACK = 0,0,0
    screen = pygame.display.set_mode((320,240))
    x = 0
    y = 1
    my_font = pygame.font.Font(None,22)
    my_lefthistory = {'Left History':(70,20)}
    my_righthistory = {'Right History':(250,20)}
    my_quit = {'QUIT':(290,200)}
    my_stop = {'STOP':(160,120)}
    my_resume = {'RESUME':(160,120)}
    my_display = {str(x):(100,20),str(y):(100,21)}
    my_history1 = [' stop      0 ','  stop      0  ','   stop      0   ']
    my_history1_pos = [(70,80),(70,120),(70,160)]
    my_history2 = [' stop      0 ','  stop      0  ','   stop      0   ']
    my_history2_pos = [(250,80),(250,120),(250,160)]
    screen.fill(BLACK)
    pygame.display.flip()
    a=time.time()
    calibrate_duration = 1.5	# no rotation
    pulse_duration = calibrate_duration
    frequency = 1000.0 / (pulse_duration + 20.0)	# frequency
    pwm_instance_1 = GPIO.PWM(channel_1, frequency)		# create a PWM instance
    pwm_instance_2 = GPIO.PWM(channel_2, frequency)		# create a PWM instance
    duty_cycle = pulse_duration * 100 / (pulse_duration + 20.0)
    pwm_instance_1.start(duty_cycle)		# where 0.0 <= duty_cycle <= 100.0
    pwm_instance_2.start(duty_cycle)		# where 0.0 <= duty_cycle <= 100.0
    state =  0
    flag = 0
    p1 = 3
    p2 = 3

    while True:
        screen.fill(BLACK)
        try:
            time.sleep(0.2)  # Without sleep, no screen output!
            for label in range(3):
                my_text = my_history2[label]
                text_pos = my_history2_pos[label]
                text_surface = my_font.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
            #x1 = str(x) 
            #y1 = str(y)
            #my_display.pop('location')
            time.sleep(0.1)
            b=time.time()
            #if (b - a > 10):
                
            elif( state == 1):
                pygame.draw.circle(screen,(0,255,0),(160,120),30,30)
                for my_text,text_pos in my_resume.items():
                    text_surface = my_font.render(my_text, True, WHITE)
                    rect = text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface,rect)
                for event in pygame.event.get():
                    if(event.type is MOUSEBUTTONDOWN):
                        pos = pygame.mouse.get_pos()
                    elif(event.type is MOUSEBUTTONUP):
                        pos = pygame.mouse.get_pos()
                        x,y = pos
                        if ( y < 160 and y > 80):
                            if ( x < 200 and x > 120):
                                state = 0
                     
                                

                        if ( y < 210 and y > 190):
                            if ( x < 300 and x > 280):
                            	pygame.quit()
               
     
        except Keyboardinterrupt:  
    	GPIO.cleanup()         

        pygame.display.flip()

def display():