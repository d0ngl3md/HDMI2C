#!/usr/bin/env python3
import pyaudio
import numpy as np
import sys
from time import sleep
from RPLCD.i2c import CharLCD
# volume up ?
# Using MCP23008 expander, with I2C address 0x50 on bus 1 for a 16x4 display.
lcd = CharLCD('MCP23008', 0x20, port=3, cols=16, rows=4, charmap='A00', auto_linebreaks=True)

# Constants
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate in Hz
BAR_MAX = 60  # if len > terminal scroling effect lol
LCD_BAR_MAX = 16 # or div max-bar by lcd length

# Turn on the backlight
lcd.backlight_enabled = True
sleep(0.5)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open microphone stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
                    
#def display_chars():
#    lcd.clear()
    

print("Listening... (Press Ctrl+C to stop)")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.linalg.norm(audio_data) / CHUNK  # Normalize volume
        bar_length = int((volume / 5000) * BAR_MAX)  # Scale bar dynamically
        bar_length = min(bar_length, BAR_MAX)  # Cap max length
        bar = "#" * bar_length  # Create ASCII bar

        sys.stdout.write(f"\r[{bar.ljust(BAR_MAX)}]")  # Print bar in place
        lcd.write_string(bar.ljust(BAR_MAX))
        sys.stdout.flush()
        lcd.clear()
        
except KeyboardInterrupt:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    lcd.close()

