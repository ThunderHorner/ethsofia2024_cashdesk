import serial
import datetime

data = [
    {'text': {'fw': 3, 'content': 'Order number: 42'.center(22)}},
    {'text': {'fw': 1, 'content': f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'}},
    {'item': {'name': 'Item 1', 'price': '2.00'}},
    {'item': {'name': 'Item 2', 'price': '14.88'}},
    {'text': {'fw': 3, 'content': '-'*24}},
    {'text': {'fw': 3, 'content': 'Total: 16.88'.rjust(22)}},
]

def format_item_line(name, price, width=48):
    return f'{name}{" " * (width - len(name) - len(price))}{price}'

def print_test_receipt(port='/dev/ttyACM0', baud=115200, timeout=0.2):
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

print_test_receipt()