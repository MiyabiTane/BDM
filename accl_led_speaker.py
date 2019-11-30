#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

#後から埋める所はhatenaと記述してあります。
import smbus
import time
import pygame.mixer
from neopixel import *
import argparse
get_time=[]

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#music= ~.mp3
def play_sound(music):
    pygame.mixer.init() #init
    pygame.mixer.music.load(music) #read
    pygame.mixer.music.play(1) #do
    time.sleep(3)
    pygame.mixer.music.stop() #finish

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

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

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

#want_to_doに実現したい光り方を入れる
# example : want_to_do=colorWipe(strip, Color(255, 0, 0))
def LED_main(want_to_do):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    try:
        while True:
            want_to_do

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

I2C_ADDR=0x1d
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

xacc_list=[];yacc_list=[];zacc_list=[]
while True:
    data = bus.read_i2c_block_data(I2C_ADDR, 0x00, 7)

    xAccl = (data[1] * 256 + data[2]) / 16
    if xAccl > 2047 :
        xAccl -= 4096
    xacc_list.append(xAccl)

    yAccl = (data[3] * 256 + data[4]) / 16
    if yAccl > 2047 :
        yAccl -= 4096
    yacc_list.append(yAccl)

    zAccl = (data[5] * 256 + data[6]) / 16
    if zAccl > 2047 :
        zAccl -= 4096
    zacc_list.append(zAccl)

    #１回目の接地では音は鳴らない
    if hatena1:#接地条件by加速度
        now_time=time.time()
        get_time.append(now_time)
        if len(get_time)>2:
            if get_time[-1]-get_time[-2]>hatena2: #hatena2:閾値その１
                play_sound(hatena3) #hatena3:ぞうの足音とか
                LED_main(hatena7) #hatena7:青色とか
            elif get_time[-1]-get_time[-2]>hatena4 and get_time[-1]-get_time[-2]<=hatena2: #hatena4:閾値その２
                play_sound(hatena5) #hatena5:普通の足音
                LED_main(hatena8) #hatena8:赤色とか
            else:
                play_sound(hatena6) #hatena6:てけてけ
                LED_main(hatena8) #hatena8:白いピカピカとか

    print("X,Y,Z-Axis : (%5d, %5d, %5d)" % (xAccl, yAccl, zAccl ))
    time.sleep(1)



#-----('Color wipe animations.')----
#colorWipe(strip, Color(255, 0, 0))  # Red wipe
#colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#colorWipe(strip, Color(0, 0, 255))  # Green wipe

#----('Theater chase animations.')----
#theaterChase(strip, Color(127, 127, 127))  # White theater chase
#theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase

#----('Rainbow animations.')----
#rainbow(strip)
#rainbowCycle(strip)
#theaterChaseRainbow(strip)
