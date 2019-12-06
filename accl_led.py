# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import numpy as np
import matplotlib.pyplot as plt
import smbus
import time
import math
from neopixel import *
import argparse

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

def disappearWipe(strip, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()/2):
        strip.setPixelColor(strip.numPixels()/2-i-1, 0)
        strip.setPixelColor(i+strip.numPixels()/2, 0)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)


I2C_ADDR=0x1C #センサが入力されている場所の設定　場所は、i2cdetect -y 1 で確認

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

print("init")

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
        
        if xAccl<=-1500 and yAccl>=1500:
            gradationblueWipe(strip)
            disappearWipe(strip)
            
        time.sleep(0.01)
