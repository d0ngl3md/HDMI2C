#!/bin/bash
# Find an addess from the available busses
# Ensure a device address argument is provided
if [[ -z "$1" ]]; then
    echo "Usage: $0 <device_address>"
    echo "Example: $0 0x28"
    exit 1
fi

dev=$1
n=$(i2cdetect -l | wc -l)

# Loop through available I2C buses and search for the device
for bus in $(seq 0 $((n-1))); do
    echo "Scanning i2c-$bus..."
    sudo i2cdetect -y -r $bus | grep -E "$dev" && echo "Device found on i2c-$bus"
done
