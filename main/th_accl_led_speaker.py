# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import numpy as np
#import matplotlib.pyplot as plt
import smbus
import time
import math
from neopixel import *
import argparse
import pygame
import threading

get_time1=[]
get_time2=[]

# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def gradationblueWipe(strip, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    color=Color(0,0,255)
    for i in range(strip.numPixels()/2):
        strip.setPixelColor(strip.numPixels()/2-i-1, color+256*17*i)
        strip.setPixelColor(i+strip.numPixels()/2, color+256*17*i)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def gradationredWipe(strip, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    color=Color(0,255,0)
    for i in range(strip.numPixels()/2):
        strip.setPixelColor(strip.numPixels()/2-i-1, color+256*256*7*i)
        strip.setPixelColor(i+strip.numPixels()/2, color+256*256*7*i)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def gradationgreenWipe(strip, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    color=Color(255,50,0)
    for i in range(strip.numPixels()/2):
        strip.setPixelColor(strip.numPixels()/2-i-1, color+256*15*i)
        strip.setPixelColor(i+strip.numPixels()/2, color+256*15*i)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def disappearWipe(strip, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()/2):
        strip.setPixelColor(strip.numPixels()/2-i-1, 0)
        strip.setPixelColor(i+strip.numPixels()/2, 0)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip, wait_ms=1, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=30):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


I2C_ADDR=0x1d #センサが入力されている場所の設定　場所は、i2cdetect -y 1 で確認

# Get I2C bus
bus = smbus.SMBus(1)

# Select Control register, 0x2A(42)
#               0x00(00)        StandBy mode
bus.write_byte_data(I2C_ADDR, 0x2A, 0x00)

# Select Control register, 0x2A(42)
#               0x01(01)        Active mode
bus.write_byte_data(I2C_ADDR, 0x2A, 0x01)

# Select Configuration register, 0x0E(14)
#               0x00(00)        Set range to +/- 2g
bus.write_byte_data(I2C_ADDR, 0x0E, 0x00)

time.sleep(0.5)

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

pygame.init()

nomal_walk=pygame.mixer.Sound("./sound/pyuko.ogg")
slow_walk=pygame.mixer.Sound("./sound/zun.ogg")
fast_walk=pygame.mixer.Sound("./sound/tetetete.ogg")

print("init")

def led_control():

    while True:
            #加速度センサのデータを代入
            data = bus.read_i2c_block_data(I2C_ADDR, 0x00, 7)
            xAccl = (data[1] * 256 + data[2]) / 16
            if xAccl > 2047 :
                xAccl -= 4096
            yAccl = (data[3] * 256 + data[4]) / 16
            if yAccl > 2047 :
                yAccl -= 4096
            zAccl = (data[5] * 256 + data[6]) / 16
            if zAccl > 2047 :
                zAccl -= 4096

            w = math.sqrt(xAccl**2 + yAccl**2 + zAccl**2) #加速度の大きさ

            if xAccl<=-1400 and yAccl>=80:
                current_time=time.time()
                get_time1.append(current_time)

                if len(get_time1)>=2:
                    print("time={}".format(get_time1[-1]-get_time1[-2]))
                    if get_time1[-1]-get_time1[-2]>1.5: #slow walk
                        gradationredWipe(strip)
                        disappearWipe(strip)
                    elif get_time1[-1]-get_time1[-2]>0.7 and get_time1[-1]-get_time1[-2]<=1.5: #nomal walk
                        gradationblueWipe(strip)
                        disappearWipe(strip)
                    else: #fast walk
                        gradationgreenWipe(strip)
                        disappearWipe(strip)

            time.sleep(0.01)

def sound_control():

    while True:
        #加速度センサのデータを代入
        data = bus.read_i2c_block_data(I2C_ADDR, 0x00, 7)
        xAccl = (data[1] * 256 + data[2]) / 16
        if xAccl > 2047 :
            xAccl -= 4096
        yAccl = (data[3] * 256 + data[4]) / 16
        if yAccl > 2047 :
            yAccl -= 4096
        zAccl = (data[5] * 256 + data[6]) / 16
        if zAccl > 2047 :
            zAccl -= 4096

        w = math.sqrt(xAccl**2 + yAccl**2 + zAccl**2) #加速度の大きさ

        if xAccl<=-1500 and yAccl>=1500:
            current_time=time.time()
            get_time2.append(current_time)

            if len(get_time2)>=2:
                if get_time2[-1]-get_time2[-2]>1.5: #slow walk
                    slow_walk.play()
                    time.sleep(1)
                elif get_time2[-1]-get_time2[-2]>0.7 and get_time2[-1]-get_time2[-2]<=1.5: #nomal walk
                    nomal_walk.play()
                    time.sleep(1)
                else: #fast walk
                    fast_walk.play()
                    time.sleep(1)

        time.sleep(0.01)

thread1=threading.Thread(target=led_control)
thread2=threading.Thread(target=sound_control)

thread1.start()
thread2.start()
