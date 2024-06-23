# app.py

from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Configuração dos pinos GPIO
control_pins = {
    17: {'name': 'UP', 'state': GPIO.LOW},
    18: {'name': 'DOWN', 'state': GPIO.LOW},
    27: {'name': 'LEFT', 'state': GPIO.LOW},
    22: {'name': 'RIGHT', 'state': GPIO.LOW}
}

read_pins = [5, 6, 13, 19]  # Pinos de leitura

GPIO.setmode(GPIO.BCM)
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in read_pins:
    GPIO.setup(pin, GPIO.IN)

@app.route("/")
def index():
    for pin in control_pins:
        control_pins[pin]['state'] = GPIO.input(pin)
    return render_template('index.html', control_pins=control_pins, read_pins=read_pins)

@app.route("/<action>/<int:pin>", methods=['POST'])
def action(action, pin):
    if action == "on":
        GPIO.output(pin, GPIO.HIGH)
        log_movimento(control_pins[pin]['name'], 'ON')
    elif action == "off":
        GPIO.output(pin, GPIO.LOW)
        log_movimento(control_pins[pin]['name'], 'OFF')
    return '', 204

@app.route("/read_pins", methods=['GET'])
def read_pins_state():
    value = 0
    for i, pin in enumerate(read_pins):
        if GPIO.input(pin) == GPIO.HIGH:
            value |= (1 << i)
    hex_value = hex(value)
    return jsonify(hex_value=hex_value)

def log_movimento(name, state):
    with open("movimentos.txt", "a") as f:
        f.write(f"{name} - {state}\n")

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
