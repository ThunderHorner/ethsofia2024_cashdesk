import re
import serial
from bleach import clean
import socketio

# Serial setup
ser = serial.Serial('/tmp/ttyV1', 115200)  # Adjust baud rate if needed

print("Listening on /tmp/ttyV1...")

# Variables to store extracted data
order_id = None
currency = "BGN"
price = None
product_name = None

# Regex pattern to capture product name and price
pattern = r'^([A-Za-z\s]+)[ ]+(\d{1,3}(?:\.\d{2}))$'

# Create a Socket.IO client instance
sio = socketio.Client()

# Event handler for connecting to the server
@sio.event
def connect():
    print("Connected to the server")

# Event handler for receiving messages from the server
@sio.on('message')
def on_message(data):
    print(f"Message received: {data}")

# Event handler for disconnecting from the server
@sio.event
def disconnect():
    print("Disconnected from the server")

# Connect to the Socket.IO server
sio.connect('http://localhost:5000')

def send_data(csv):
    # Send the CSV data via Socket.IO
    sio.emit('message', csv)

while True:
    if ser.in_waiting > 0:
        line = ser.readline()
        clean_line = line.decode('utf-8').rstrip()

        # Capture order number
        if 'Order number' in clean_line:
            order_id = clean_line.split('Order number:')[1].strip()
            price = None
            product_name = None
            print(f"Order ID: {order_id}")

        # Match product name and price
        match = re.match(pattern, clean_line)
        if match:
            product_name = match.group(1).strip()
            price = float(match.group(2))
            print(f"Product Name: {product_name}, Price: {price} {currency}")

        # Forward the line to the printer
        with serial.Serial('/dev/ttyACM0', 115200, timeout=.1) as printer:
            printer.write(line)

        # Send data when both product name and price are available
        if product_name and price:
            csv = ','.join(map(str, [order_id, currency, price, product_name]))
            send_data(csv)
