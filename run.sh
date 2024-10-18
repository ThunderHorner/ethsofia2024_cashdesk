#!/bin/bash

cleanup() {
    echo "Stopping all services..."
    kill $cashdesk_pid $printer_server_pid $serial_proxy_pid
    echo "All services stopped."
}

trap cleanup EXIT

echo "Starting services..."

cd cashdesk-mock && npm start &
cashdesk_pid=$!

cd ../thermal-printer

python thermal_printer/init_virtual_ports.sh &
python thermal_printer/thermal_printer_server.py &
printer_server_pid=$!
python thermal_printer/serial_proxy.py &
serial_proxy_pid=$!

wait