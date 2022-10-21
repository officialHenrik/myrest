#!/usr/bin/env python3

from flask import Flask, jsonify, request, render_template
import os
import threading
import time
import numpy as np
import random

app = Flask(__name__)

batch = [
    {
        'id': 1,
        'name': u'SensorX',
        'value': 0
    },
    {
        'id': 2,
        'name': u'SensorSine',
        'value': 0
    }
]

hello_word = 'world'
sine_gain = 100


# curl 127.0.0.1:5000/api/v1.0/hello?word=fjant
# curl 127.0.0.1:5000/api/v1.0/hello
@app.route("/api/v1.0/hello", methods=['GET'])
def hello():
    global hello_word
    tmp = request.args.get('word')
    if tmp:
        hello_word = tmp
    return "Hello " + hello_word + " !"


# curl 127.0.0.1:5000/api/v1.0/sensors
# curl 127.0.0.1:5000/api/v1.0/sensors?id=1
@app.route('/api/v1.0/sensors', methods=['GET'])
def get_sensor_readings():

    id = request.args.get('id')
    if not id:
        return jsonify({'batch': batch})
    try:
        idx = int(id)-1
    except ValueError:
        return "INVALID INDEX"

    if len(batch) > idx:
        return str(batch[idx]["value"])
    else:
        return "INVALID INDEX"


# curl 127.0.0.1:5000/api/v1.0/sine?gain=100
@app.route('/api/v1.0/sine', methods=['GET'])
def set_sine_gain():
    global sine_gain

    gain = request.args.get('gain')
    if gain:
        g = gain
    else:
        return "INVALID GAIN"
    try:
        g = int(g)
    except ValueError:
        return "INVALID GAIN"

    sine_gain = g
    return "Sine gain: " + str(sine_gain)


# Retrieve the home page for the app
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", sine_val=round(batch[1]["value"], 2))


# Fake sensor
def sensor_sampler():
    while 1:
        batch[0]["value"] += 0.01
        x = batch[0]["value"]
        batch[1]["value"] = np.sin(x) * sine_gain
        time.sleep(0.1)


if __name__ == '__main__':

    x = threading.Thread(target=sensor_sampler)
    x.daemon = True
    x.start()

    app.run(debug=True, host='10.44.18.33', port=5000)
