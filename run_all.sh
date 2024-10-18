#!/bin/bash

# Activate the virtual environment
source bin/activate

# Trap for Ctrl+C
trap "kill 0" EXIT

# Run the WebSocket server in the background
./thermal_printer/init_virtual_ports.sh &
sleep 5

# Run the run.sh script in the background
./run.sh &

# Wait for all processes to finish
wait
