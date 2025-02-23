#!/usr/bin/env python3
from time import sleep
from RPLCD.i2c import CharLCD
# pip install RPLCD
# pip install smbus2
# run the setup script, or install i2c-tools, and set premissions.
#lcd = CharLCD('PCF8574', 0x50, port=1, cols=16, rows=2, charmap='A00', auto_linebreaks=True)
lcd = CharLCD('MCP23008', 0x20, port=3, cols=16, rows=4, charmap='A00', auto_linebreaks=True)

# Turn on the backlight.
lcd.backlight_enabled = True
sleep(1)
try:
    counter = 0
    while True:
        # Clear the display before updating
        lcd.clear()
        
        # Write "Hello World!" on the first row
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Hello World!")
        
        # Write the seconds count on the second row
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Count: {}".format(counter))
        
        counter += 1
        sleep(1)
except KeyboardInterrupt:
    lcd.clear()
'''
Useful links:
https://github.com/dbrgn/RPLCD
https://dave.cheney.net/2014/08/03/tinyterm-a-silly-terminal-emulator-written-in-go
'''
