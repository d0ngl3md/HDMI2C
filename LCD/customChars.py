#!/usr/bin/env python3
from time import sleep
from RPLCD.i2c import CharLCD
# volume up ?
# Using MCP23008 expander, with I2C address 0x50 on bus 1 for a 16x4 display.
lcd = CharLCD('MCP23008', 0x20, port=3, cols=16, rows=4, charmap='A00', auto_linebreaks=True)

# Define custom character byte arrays easier to see in glyphs, but fewer lines like this so...
AL_CHARS = [
    [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],  # AL1
    [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111],  # AL2
    [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111, 0b11111],  # AL3
    [0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111, 0b11111, 0b11111],  # AL4
    [0b00000, 0b00000, 0b00000, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],  # AL5
    [0b00000, 0b00000, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],  # AL6
    [0b00000, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111],  # AL7
    [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111]   # AL8
]
# on a typical lcd 16x2 you have space for 8 custom chars. does 16x4 have more mem? remember to test that later.

HL_CHARS = [
    [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],  # AL1
    [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000],  # AL2
    [0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000, 0b11000],  # AL3
    [0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100, 0b11100],  # AL4
    [0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110, 0b11110],  # AL5
    [0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111]   # AL6

]
# Turn on the backlight
lcd.backlight_enabled = True
sleep(0.5)

# Store the custom characters in LCD memory
for i, char in enumerate(AL_CHARS):
    lcd.create_char(i, char)


def display_chars():
    lcd.clear()
    lcd.write_string('BUMP: ')
    for i in range(len(AL_CHARS)):
        lcd.write_string(chr(i)) 
        sleep(i/9)  

try:
    while True:
        display_chars()
        sleep(1)  
except KeyboardInterrupt:
    print("\nStopping LCD display...")
    lcd.close()
