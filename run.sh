#!/bin/bash

cleanup() {
    echo "Stopping all services..."
    kill $cashdesk_pid $printer_server_pid
    wait $cashdesk_pid $printer_server_pid 2>/dev/null
    echo "All services stopped."
}

trap cleanup EXIT

echo "Starting services..."

# Start the cashdesk-mock service
cd cashdesk-mock && npm start &
cashdesk_pid=$!
if [ -z "$cashdesk_pid" ]; then
    echo "Failed to start cashdesk-mock."
    exit 1
fi

# Start the thermal printer server
cd ../thermal-printer
python thermal_printer/thermal_printer_server.py &
printer_server_pid=$!
if [ -z "$printer_server_pid" ]; then
    echo "Failed to start thermal printer server."
    exit 1
fi

echo "All services started successfully."

# Wait for all services to complete or stop
wait
