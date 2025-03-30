#!/usr/bin/env python3
from smbus2 import SMBus, i2c_msg
import struct
import time
'''
https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/pinouts
or read Adafruit_seesaw.h from aruino libs
'''

I2C_BUS = 7          # May change from system to system
I2C_ADDR = 0x36
SEESAW_ENCODER_BASE = 0x11
SEESAW_ENCODER_POSITION = 0x30
SEESAW_ENCODER_DELTA = 0x40

def read_register(bus, base, reg, length):
    # Write base + reg
    write = i2c_msg.write(I2C_ADDR, [base, reg])
    read = i2c_msg.read(I2C_ADDR, length)
    bus.i2c_rdwr(write, read)
    return list(read)

def read_encoder_position(bus):
    data = read_register(bus, SEESAW_ENCODER_BASE, SEESAW_ENCODER_POSITION, 4)
    pos = struct.unpack(">i", bytes(data))[0]
    return pos

def read_encoder_delta(bus):
    data = read_register(bus, SEESAW_ENCODER_BASE, SEESAW_ENCODER_DELTA, 4)
    delta = struct.unpack(">i", bytes(data))[0]
    return delta

if __name__ == "__main__":
    with SMBus(I2C_BUS) as bus:
        try:
            while True:
                pos = read_encoder_position(bus)
                delta = read_encoder_delta(bus)
                print(f"Position: {pos}, Delta: {delta}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
