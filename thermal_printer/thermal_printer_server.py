from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import serial
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Format item lines for the receipt
def format_item_line(name, price, width=48):
    return f'{name}{" " * (width - len(name) - len(price))}{price}'

# Endpoint to receive receipt data and print it
@app.route('/print-receipt', methods=['POST'])
def print_receipt():
    try:
        data = request.json
        order_number = data.get('orderNumber')
        items = data.get('items')
        total = data.get('total')

        # Create receipt structure
        receipt_data = [
            {'text': {'fw': 3, 'content': f'Order number: {order_number}'.center(22)}},
            {'text': {'fw': 1, 'content': f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}' }},
        ]

        # Add each item to the receipt
        for item in items:
            receipt_data.append({'item': {'name': item['ProductName'], 'price': str(item['Price'])}})

        receipt_data.append({'text': {'fw': 3, 'content': '-' * 24}})
        receipt_data.append({'text': {'fw': 3, 'content': f'Total: {total}'.rjust(22)}})

        # Send receipt to printer
        print_to_printer(receipt_data)

        return jsonify({"message": "Receipt printed successfully"}), 200

    except Exception as e:
        print(f"Error printing receipt: {e}")
        return jsonify({"error": "Failed to print receipt"}), 500

# Function to print receipt to serial printer
def print_to_printer(data, port='/dev/ttyACM0', baud=115200, timeout=0.2):
    with serial.Serial(port, baud, timeout=timeout) as ser:
        font_commands = {
            0: b'\x1B\x21\x00',  # Normal
            1: b'\x1B\x21\x00',  # Normal (small)
            2: b'\x1B\x21\x10',  # Double height
            3: b'\x1B\x21\x30',  # Large (double width and height)
        }

        for item in data:
            if 'text' in item:
                ser.write(font_commands[item['text']['fw']])
                ser.write(item['text']['content'].encode('utf-8'))
            elif 'item' in item:
                ser.write(font_commands[0])
                content = format_item_line(item['item']['name'], item['item']['price'])
                ser.write(content.encode('utf-8'))
            ser.write(b'\n')
            ser.write(font_commands[0])

        ser.write(b'\n' * 5)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
