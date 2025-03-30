#!/bin/bash
# Find an addess from the available busses
# Ensure a device address argument is provided
if [[ -z "$1" ]]; then
   echo "No Address provided. ... Scanning all addresses"
   # echo "Usage: $0 <device_address>"
   # echo "Example: $0 0x28"

   n=$(i2cdetect -l | wc -l)
for bus in $(seq 0 $((n-1))); do
    #echo "Scanning i2c-$bus..."
    sudo i2cdetect -y -r $bus 
done
    exit 1
fi

dev=$1
n=$(i2cdetect -l | wc -l)

# Loop through available I2C buses and search for the device
for bus in $(seq 0 $((n-1))); do
    echo "Scanning i2c-$bus..."
    sudo i2cdetect -y -r $bus | grep -E "$dev" && echo "Device found on i2c-$bus"
done

# debating to have a log creation function.
# scanning all addresses can be slow.
# but maybe a log could be useful for other reasons, like to do a diff
# or to speed up finding when a stubborn device doesnt init right away.
#
# A cloned dev box could break that logic, then again an erratic device could break that logic too.
# ok Ima do it. later.
