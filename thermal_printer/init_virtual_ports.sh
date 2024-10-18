#!/bin/bash

# Create a virtual serial port pair
socat -d -d pty,raw,echo=0,link=/tmp/ttyV0 pty,raw,echo=0,link=/tmp/ttyV1 &

# Forward data between the real and virtual ports
socat -d -d /dev/ttyACM0,raw,echo=0,b115200 /tmp/ttyV0,raw,echo=0 &

echo "Virtual serial ports created:"
echo "Original port: /dev/ttyACM0"
echo "Virtual port for your Python server: /tmp/ttyV0"
echo "Virtual port for listening: /tmp/ttyV1"