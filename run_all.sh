#!/bin/bash

# Open the first tab and run the first command
gnome-terminal --tab --title="Init Virtual Ports" -- bash -c "sh thermal_printer/init_virtual_ports.sh; exec bash"

# Open the second tab and run the second command in the same terminal window
gnome-terminal --tab --title="Run Script" -- bash -c "./run.sh; exec bash"
