#!/usr/bin/env python
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math
import pygame
from pygame.locals import*
import globalname

base_rhy = 0.05
high_basic = [320,40]
low_basic = [320,80]

def appendnote(key,note_duration,keys):
    note_length = note_duration / base_rhy
    if(keys.index(key) <= 1):
        keypos = 1
        rise = keys.index(key) - keypos
    elif(keys.index(key) <= 3):
        keypos = 2
        rise = keys.index(key) - keypos - 1
    elif(keys.index(key) <= 4):
        keypos = 3
        rise = keys.index(key) - keypos - 1
    elif(keys.index(key) <= 6):
        keypos = 4
        rise = keys.index(key) - keypos - 2
    elif(keys.index(key) <= 8):
        keypos = 5
        rise = keys.index(key) - keypos - 3
    elif(keys.index(key) <= 10):
        keypos = 6
        rise = keys.index(key) - keypos - 4
    elif(keys.index(key) <= 11):
        keypos = 7
        rise = 0
    location = globalname.mainlocation - keypos*3
    #print (math.ceil(note_length), location )
    globalname.notelist.append([math.ceil(note_length),location,320])
    #print (globalname.notelist)

    '''score_ = pygame.image.load("score_high.png")
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

        pygame.display.flip()'''
        
def appendrest(note_duration):
    rest_length = note_duration / base_rhy 
    if (math.floor(rest_length) > 2 ):
        globalname.notelist.append([math.floor(rest_length),99,320])
    #location = globalname.mainlocation * 12 + keys.index(key)

def displaybase(screen):
    score = pygame.image.load("./notelib/base.png")
    score = pygame.transform.scale(score,(320,120))
    screen.blit(score,(0,40))

def displaynote(screen):
    #pass
    speed = 1.5
    if( globalname.notelist[0][2] < 80):
        globalname.notelist.pop(0)
    for i in globalname.notelist:
        if( i[1]!= 99 ):
            if (i[0] <= 2 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/sixteenth_note.png")
                screen.blit(note,(i[2],i[1]))
            elif (i[0] <= 4 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/eighth_note.png")
                screen.blit(note,(i[2],i[1]))
            elif (i[0] <= 8 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/quarter_note.png")
                screen.blit(note,(i[2],i[1]))
            elif (i[0] <= 16 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/half_note.png")
                screen.blit(note,(i[2],i[1]))
            elif (i[0] <= 32 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/whole_note.png")
                screen.blit(note,(i[2],i[1]))
            else:
                i[2] = i[2] - speed
        else:
            if (i[0] <= 2 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/sixteenth_rest.png")
                screen.blit(note,(i[2]+30,50))
            elif (i[0] <= 4 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/eighth_rest.png")
                screen.blit(note,(i[2]+30,50))
            elif (i[0] <= 8 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/quarter_rest.png")
                screen.blit(note,(i[2]+30,50))
            else:
                i[2] = i[2] - speed
                #else:

                
                
    print (globalname.notelist)
    
    #for notelength,notelocation in globalname.notelist.items()
    

#def note_type(note_length,tune_length):


