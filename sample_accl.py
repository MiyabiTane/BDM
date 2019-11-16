# Based on https://github.com/ControlEverythingCommunity/MMA8452Q/blob/master/Python/MMA8452Q.py

import smbus
import time

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

while True:
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

    print("X,Y,Z-Axis : (%5d, %5d, %5d)" % (xAccl, yAccl, zAccl ))
    print(xAccl)
    time.sleep(1)
