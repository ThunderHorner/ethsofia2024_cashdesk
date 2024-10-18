from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

@app.route('/')
def index():
    return "Socket.IO server is running!"

@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")
    socketio.emit('message', msg)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)

