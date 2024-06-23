# app.py

from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configurar os pinos GPIO
pins = {
    17: {'name': 'UP', 'state': GPIO.LOW},
    18: {'name': 'DOWN', 'state': GPIO.LOW},
    27: {'name': 'LEFT', 'state': GPIO.LOW},
    22: {'name': 'RIGHT', 'state': GPIO.LOW}
}

GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def index():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    return render_template('index.html', pins=pins)

@app.route("/<action>/<int:pin>")
def action(action, pin):
    if action == "on":
        GPIO.output(pin, GPIO.HIGH)
        log_movimento(pins[pin]['name'], 'ON')
    elif action == "off":
        GPIO.output(pin, GPIO.LOW)
        log_movimento(pins[pin]['name'], 'OFF')
    return '', 204

def log_movimento(name, state):
    with open("movimentos.txt", "a") as f:
        f.write(f"{name} - {state}\n")

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
