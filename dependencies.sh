echo "This script will modify your Raspberry Pi OS installation"
echo "It will do the following:"
echo "1. Enable I2C"
echo "2. Enable SPI"
echo "3. Enable UART"
echo "4. Disable bluetooth"

read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    if hash raspi_config 2>/dev/null; then
    echo "'raspi_config' could not be found. Are you running Raspberry Pi OS?"
    exit 1
else
    sudo raspi_config nonint do_i2c 0   # Enable I2C
    sudo raspi_config nonint do_spi 0   # Enable SPI
    sudo dtoverlay disable_bt  # disable BT
    sudo raspi-config nonint do_serial_hw 0  # Enable UART on BT port
fi
fi


