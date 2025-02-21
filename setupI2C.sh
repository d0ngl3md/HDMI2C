#!/bin/bash
# admitedly, this is only for deb based linux. tested on mint, ubuntu
# Required packages
pkgz=("i2c-tools" "python3-smbus" "libi2c-dev")

echo "Checking for required packages..."
MISSING_PACKAGES=()

# Check for each package
for pkg in "${pkgz[@]}"; do
    if ! dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "install ok installed"; then
        echo "Missing: $pkg"
        MISSING_PACKAGES+=("$pkg")
    fi
done

# Install missing packages if any are missing
if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "Installing missing packages: ${MISSING_PACKAGES[*]}"
    sudo apt update && sudo apt install -y "${MISSING_PACKAGES[@]}"
else
    echo "All required packages are installed."
fi

# Load i2c-dev kernel module without reboot
echo "Checking if i2c-dev module is loaded..."
if ! lsmod | grep -q "^i2c_dev"; then
    echo "i2c-dev module is not loaded. Loading it now..."
    sudo modprobe i2c-dev
    echo "i2c-dev" | sudo tee -a /etc/modules >/dev/null
else
    echo "i2c-dev module is already loaded."
fi

# Ensure i2c group exists
if ! getent group i2c >/dev/null; then
    echo "Creating i2c group..."
    sudo groupadd i2c
else
    echo "i2c group already exists."
fi

# Check if the user is in the i2c group
echo "Checking user group permissions..."
if groups | grep -q "\bi2c\b"; then
    echo "User $USER is already in the i2c group."
else
    echo "Adding user to the i2c group..."
    sudo usermod -aG i2c "$USER"
    exec sg i2c "$SHELL"
fi

# Set device permissions immediately
echo "Setting up permissions for I2C devices..."
sudo chown root:i2c /dev/i2c-* 2>/dev/null
sudo chmod 660 /dev/i2c-* 2>/dev/null

# Add Udev rule for persistent permissions
UDEV_RULE_FILE="/etc/udev/rules.d/99-i2c.rules"
echo "Checking for existing udev rule..."
if ! grep -q 'KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"' "$UDEV_RULE_FILE" 2>/dev/null; then
    echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"' | sudo tee "$UDEV_RULE_FILE" >/dev/null
    sudo udevadm control --reload-rules && sudo udevadm trigger
    echo "Udev rules updated and reloaded."
else
    echo "Udev rule already exists."
fi

echo "I2C setup complete. You can use I2C devices now!"
