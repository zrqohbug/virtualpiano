#!/usr/bin/env python
import os
import RPi.GPIO as GPIO
import time
import subprocess
import math
import pygame
from pygame.locals import*
import globalname

base_rhy = 0.15
high_basic = [320,40]
low_basic = [320,80]


def appendnote(key,note_duration,keys):
    note_length = (note_duration + 0.05 ) / base_rhy
    localpos = globalname.mainlocation * 12 + keys.index(key)
    if (localpos >= 0 and localpos <= 10):
        pngpos = 1
    elif (localpos >= -10 and localpos <= -1):
        pngpos = 0
    elif (localpos < -6 ):
        pngpos = 1
    else:
        pngpos = 0
    if(keys.index(key) <= 1):
        keypos = 1
        rise = keys.index(key) - keypos + 1
    elif(keys.index(key) <= 3):
        keypos = 2
        rise = keys.index(key) - keypos - 0
    elif(keys.index(key) <= 4):
        keypos = 3
        rise = keys.index(key) - keypos - 1
    elif(keys.index(key) <= 6):
        keypos = 4
        rise = keys.index(key) - keypos - 1
    elif(keys.index(key) <= 8):
        keypos = 5
        rise = keys.index(key) - keypos - 2
    elif(keys.index(key) <= 10):
        keypos = 6
        rise = keys.index(key) - keypos - 3
    elif(keys.index(key) <= 11):
        keypos = 7
        rise = 0
    location = globalname.locationheight - globalname.mainlocation * 21 - keypos*3    # has 7 note from C to C
    if globalname.mainlocation < 0:
        location = location + 22                  #need to modify
    #print (math.ceil(note_length), location )
    note_start_point = math.ceil(note_length) * 3
    line_number = short_line(location,keypos,keys.index(key))
    #print(line_number)
    globalname.notelist.append([math.ceil(note_length) , location , 320 - note_start_point ,rise,line_number,pngpos])
    #print (globalname.notelist)
        
def appendrest(note_duration):
    rest_length = ( note_duration - 0.05 ) / base_rhy 
    #if (math.floor(rest_length) > 3 ):
    globalname.notelist.append([math.floor(rest_length),99,320 - findlength(rest_length) * 1.5,0])
    #location = globalname.mainlocation * 12 + keys.index(key)

def displaykey(screen):
    keyboard = pygame.image.load("./notelib/keyboard/1_0.jpg")
    keyboard = pygame.transform.scale(keyboard,(320,80))
    screen.blit(keyboard,(0,160))     

def displaykeyboard(key,keys,screen):
    if ( keys.index(key) == 0 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_1.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 1 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_2.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 2 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_3.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 3 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_4.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 4 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_5.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 5 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_6.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 6 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_7.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 7 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_8.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160)) 
    if ( keys.index(key) == 8 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_9.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 9 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_10.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 10 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_11.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160))
    if ( keys.index(key) == 11 ):
        keyboard = pygame.image.load("./notelib/keyboard/1_12.jpg")
        keyboard = pygame.transform.scale(keyboard,(320,80))
        screen.blit(keyboard,(0,160)) 
        
    
def displaybase(screen):
    score = pygame.image.load("./notelib/base.png")
    score = pygame.transform.scale(score,(320,120))
    screen.blit(score,(0,globalname.locationheight - 9))
    globalname.count1 += 1
    globalname.count2 += 1
    speed = 0.6
    location1 = 320 - globalname.count1 * speed
    #print (globalname.count1,globalname.count2)
    if globalname.count1 > 200:
        globalname.count1 = 0 
    location2 = 320 - globalname.count2 * speed
    if globalname.count2 > 200:
        globalname.count2 = 0 
        
    line1 = pygame.image.load("./notelib/line.png")
    line1 = pygame.transform.scale(line1,(4,88))
    #screen.blit(line1,(location1, globalname.locationheight + 10))
    '''line2 = pygame.image.load("./notelib/line.png")
    line2 = pygame.transform.scale(line2,(4,88))
    screen.blit(line2,(location2,59))  '''

def displaynote(screen):
    #pass
    speed = 3
    if( not globalname.notelist ):
        globalname.notelist.append([0,0,0])
    if( globalname.notelist[0][2] < 80):
        globalname.notelist.pop(0)

    for i in globalname.notelist:
        #print (i)
        if( i[1]!= 99 ):
            if( i[4] != 100):
                line = pygame.image.load("./notelib/line2.png")
                line = pygame.transform.scale(line,(15,8))
                if (i[4] > 0):
                    for k in range(1,i[4]+1):
                        screen.blit(line,(i[2]+7,i[1] - k*3 + 43 ))
                if (i[4] == 0 ):
                    #line = pygame.image.load("./notelib/line2.png")
                    screen.blit(line,(i[2]+1,i[1]+ 45))
                if (i[4] < 0):
                    for k in range(1,-i[4]+1):
                        #print(k)
                        #line = pygame.image.load("./notelib/line2.png")
                        screen.blit(line,(i[2]+1,i[1] + k*6 + 38))              
            note_start_point = 0
            if (i[0] <= 2 ):
                i[2] = i[2] - speed
                if ( i[5] == 1):
                    note = pygame.image.load("./notelib/sixteenth_note.png")
                    screen.blit(note,(i[2],i[1]))
                else:
                    note = pygame.image.load("./notelib/sixteenth_note2.png")
                    screen.blit(note,(i[2],i[1]+31))                  
                #globalname.count += 2
            elif (i[0] <= 4 ):
                i[2] = i[2] - speed
                if( i[5] == 1):
                    note = pygame.image.load("./notelib/eighth_note.png")
                    screen.blit(note,(i[2],i[1]))
                else:
                    note = pygame.image.load("./notelib/eighth_note2.png")
                    screen.blit(note,(i[2],i[1]+25))                     
                #globalname.count += 4
            elif (i[0] <= 8 ):
                i[2] = i[2] - speed
                if( i[5] == 1):
                    note = pygame.image.load("./notelib/quarter_note.png")
                    screen.blit(note,(i[2],i[1]))
                else:
                    note = pygame.image.load("./notelib/quarter_note2.png")
                    screen.blit(note,(i[2],i[1]+31))                    
                #globalname.count += 8
            elif (i[0] <= 16 ):
                i[2] = i[2] - speed
                if( i[5] == 1):                
                    note = pygame.image.load("./notelib/half_note.png")
                    screen.blit(note,(i[2],i[1]))
                else:
                    note = pygame.image.load("./notelib/half_note2.png")
                    screen.blit(note,(i[2],i[1]+31))   
                #globalname.count += 16
                '''elif (i[0] <= 32 ):
                i[2] = i[2] - speed
                note = pygame.image.load("./notelib/whole_note.png")
                screen.blit(note,(i[2],i[1]))'''
                #globalname.count += 32
            else:
                i[2] = i[2] - speed
                #if( i[5] == 1):         
                note = pygame.image.load("./notelib/whole_note.png")
                screen.blit(note,(i[2],i[1]))
                
                
            if (i[3] == 1):
                if(i[5] == 1):
                    rise = pygame.image.load("./notelib/rise.png")
                    rise = pygame.transform.scale(rise,(8,16))
                    screen.blit(rise,(i[2]-3,i[1]+41))
                else:
                    rise = pygame.image.load("./notelib/rise.png")
                    rise = pygame.transform.scale(rise,(8,16))
                    screen.blit(rise,(i[2]  ,i[1]+37))                 
                
        else:
            if globalname.mainlocation < 0:
                location = globalname.locationheight + 62
            else:
                location = globalname.locationheight
            if (math.floor(i[0]) > 3 ):
                if (i[0] <= 2 ):
                    i[2] = i[2] - speed
                    note = pygame.image.load("./notelib/sixteenth_rest.png")
                    screen.blit(note,(i[2],location + 2))
                elif (i[0] <= 4 ):
                    i[2] = i[2] - speed
                    note = pygame.image.load("./notelib/eighth_rest.png")
                    screen.blit(note,(i[2],location + 2))
                elif (i[0] <= 8 ):
                    i[2] = i[2] - speed
                    note = pygame.image.load("./notelib/quarter_rest.png")
                    screen.blit(note,(i[2],location + 2))
                elif (i[0] <= 16 ):
                    i[2] = i[2] - speed
                    note = pygame.image.load("./notelib/quarter_rest.png")
                    screen.blit(note,(i[2],location + 2))
                elif (i[0] <= 32 ):
                    i[2] = i[2] - speed
                    note = pygame.image.load("./notelib/quarter_rest.png")
                    screen.blit(note,(i[2],location + 2))
                else:
                    i[2] = i[2] - speed                    
            else:
                i[2] = i[2] - speed
                    #else:

def findlength(act_length):
    if (act_length <= 2 ):
        return 2
    elif (act_length <= 4 ):
        return 4
    elif (act_length <= 8 ):
        return 8
    elif (act_length <= 16 ):
        return 16
    elif (act_length <= 32 ):
        return 32
    else:
        return 64
                
    #print (globalname.notelist)
    
    #for notelength,notelocation in globalname.notelist.items()

def short_line(location,keypos,keyind):
    shortline = 100
    if(globalname.mainlocation == 2):
        shortline = 2 + math.floor(keypos / 2)
    elif(globalname.mainlocation == 1):
        if(keypos == 6 or keypos == 7 ):
            shortline = 1
    elif(globalname.mainlocation == 0):
        if(keyind == 0):
            shortline = 0
        if(keyind == 1):
            shortline = 0
    elif(globalname.mainlocation == -2):
        if(keyind == 0):
            shortline = -2
        if(keyind == 1):
            shortline = -2
        if(keyind == 2):
            shortline = -1
        if(keyind == 3):
            shortline = -1
    #print (keyind)
    return shortline

#def note_type(note_length,tune_length):


