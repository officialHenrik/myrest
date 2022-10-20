#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os, threading, time
import numpy as np

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

# Fake sensor
def sensor_sampler():
    while 1:
        batch[0]["value"]+=0.01
        x = batch[0]["value"]
        batch[1]["value"]=np.sin(x)*100
        time.sleep(0.1)

if __name__ == '__main__':
    
    x = threading.Thread(target=sensor_sampler)
    x.daemon = True
    x.start()
    
    app.run(debug=True, host='10.44.18.33', port=5000)