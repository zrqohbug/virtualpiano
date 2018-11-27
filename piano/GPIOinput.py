#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import piano
import globalname

def input():
    return globalname.n
    
def GPIO5_both(channel):
    if (GPIO.input(5) == False):
        globalname.n = [99,5]
    if (GPIO.input(5) == True):
        globalname.n = [100,5]

def GPIO6_both(channel):
    if (GPIO.input(6) == False):
        globalname.n = [99,6]
    if (GPIO.input(6) == True):
        globalname.n = [100,6]

def GPIO12_both(channel):
    if (GPIO.input(12) == False):
        globalname.n = [99,12]
    if (GPIO.input(12) == True):
        globalname.n = [100,12]

def GPIO13_both(channel):
    if (GPIO.input(13) == False):
        globalname.n = [99,13]
    if (GPIO.input(13) == True):
        globalname.n = [100,13]
            
def GPIO16_both(channel):
    if (GPIO.input(16) == False):
        globalname.n = [99,16]
    if (GPIO.input(16) == True):
        globalname.n = [100,16]   
            
def GPIO17_both(channel):
    #print('1234')
    if (GPIO.input(17) == False):
        #print('12354')        
        globalname.n = [99,17]
    if (GPIO.input(17) == True):
        globalname.n = [100,17]
                
def GPIO18_both(channel):
    if (GPIO.input(18) == False):
        globalname.n = [99,18]
    if (GPIO.input(18) == True):
        globalname.n = [100,18]
            
def GPIO19_both(channel):
    if (GPIO.input(19) == False):
        globalname.n = [99,19]
    if (GPIO.input(19) == True):
        globalname.n = [100,19]  
            
def GPIO20_both(channel):
    if (GPIO.input(20) == False):
        globalname.n = [99,20]
    if (GPIO.input(20) == True):
        globalname.n = [100,20]
            
def GPIO21_both(channel):
    if (GPIO.input(21) == False):
        globalname.n = [99,21]
    if (GPIO.input(21) == True):
        globalname.n = [100,21]
            
def GPIO22_both(channel):
    if (GPIO.input(22) == False):
        globalname.n = [99,22]
    if (GPIO.input(22) == True):
        globalname.n = [100,22]
            
def GPIO23_both(channel):
    if (GPIO.input(23) == False):
        globalname.n = [99,23]
    if (GPIO.input(23) == True):
        globalname.n = [100,23]
            
def GPIO26_both(channel):
    if (GPIO.input(26) == False):
        globalname.n = [99,26]
    if (GPIO.input(26) == True):
        globalname.n = [100,26]

def GPIO27_both(channel):
    if (GPIO.input(27) == False):
        globalname.n = [99,27]
    if (GPIO.input(27) == True):
        globalname.n = [100,27]
            