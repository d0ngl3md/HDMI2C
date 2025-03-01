# HDMI2C
My adventure into I2C devices over HDMI
after running set up script, you are in i2c group, but .. theres a glitchy thing, might need need to log out and back in, though you are now member to the i2c group. as a member to the i2c group, with group ownership over the i2c devices, you should not need root to run programs accessing the i2c bus. thats the thought anyway. 

STEMMA 4-Pin I2C (both standard & STEMMA QT) <br>
<br>Black for GND. 
<br>Red for V+ 
<br>Blue for SDA. 
<br>Yellow for SCL

<br>
I just obsurved a singular device with several addresses, might try to write that into a serach option.
<br>
LCD 16x4, i2c base addresses, 0x20 thru 0x27
<br><br>
I had been messing with this on a display port to HDMI addapter, and could not get it to work.
When I switched over to a straight throught HDMI, it worked instantly!
<br>
sudo apt-install python3-dev
pip install spidev

 
