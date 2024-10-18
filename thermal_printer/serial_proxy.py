import re
import serial
import socketio
from serial.tools import list_ports

# Constants
SERIAL_PORT = '/tmp/ttyV1'
BAUD_RATE = 115200
PRINTER_PORT = '/dev/ttyACM0'
SOCKET_IO_SERVER = 'http://localhost:5000'
DEFAULT_CURRENCY = "BGN"

# Regex pattern to capture product name and price

PRODUCT_PATTERN = r'^([\w\s]+)\s+(\d{1,3}\.\d{2})$'



class OrderProcessor:
    def __init__(self):
        self.order_id = None
        self.currency = DEFAULT_CURRENCY
        self.price = None
        self.product_name = None
        self.sio = socketio.Client()
        self.setup_socket_io()

    def setup_socket_io(self):
        @self.sio.event
        def connect():
            print("Connected to the server")

        @self.sio.on('message')
        def on_message(data):
            print(f"Message received: {data}")

        @self.sio.event
        def disconnect():
            print("Disconnected from the server")

        self.sio.connect(SOCKET_IO_SERVER)

    def process_line(self, line):
        clean_line = line.decode('utf-8').strip()
        print(f"line {line}")
        print(f"line {clean_line}")
        if 'Order number' in clean_line:
            self.order_id = clean_line.split('Order number:')[1].strip()
            self.price = None
            self.product_name = None
            # print(f"Order ID: {self.order_id}")
        else:
            result = re.search(PRODUCT_PATTERN, 'Product  123            10.00')

            if result:
                product_name = result.group(1).strip()  # First group is the product name
                price = result.group(2)  # Second group is the price

                # print(f'Product Name: "{product_name}", Price: {price}')
                # print(product_line)
                self.product_name = product_name
                self.price = price
                # print(f"Product Name: {self.product_name}, Price: {self.price} {self.currency}")
                self.send_data(self.order_id, self.price, self.product_name)

        self.forward_to_printer(line)

    def send_data(self, order_id, price, product_name):
        # if self.product_name and self.price:
        csv = ','.join(map(str, [order_id, self.currency, price, product_name]))
        self.sio.emit('message', csv)

    @staticmethod
    def forward_to_printer(line):
        # return
        try:
            with serial.Serial(PRINTER_PORT, BAUD_RATE, timeout=.1) as printer:
                printer.write(line)
        except serial.SerialException as e:
            print(f"Error forwarding to printer: {e}")

def find_serial_port(port_hint):
    available_ports = list_ports.comports()
    for port in available_ports:
        if port_hint in port.device:
            return port.device
    return None

def main():
    serial_port = find_serial_port(SERIAL_PORT) or SERIAL_PORT
    print(f"Listening on {serial_port}...")

    processor = OrderProcessor()

    try:
        with serial.Serial(serial_port, BAUD_RATE, timeout=2) as ser:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline()
                    processor.process_line(line)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        processor.sio.disconnect()

if __name__ == "__main__":
    main()