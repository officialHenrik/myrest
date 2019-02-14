#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os

app = Flask(__name__)

batch = [
{
  'id': 1,
  'name': u'Sensor1',
  'values': u'1, 12, 27, 13, 111',
},
{
  'id': 2,
  'name': u'Sensor2',
  'values': u'3, 5, 67, 14, 132'
}
]

hello_word = 'world'

# curl 127.0.0.1:5000/todo/api/v1.0/hello?word=fjant
# curl 127.0.0.1:5000/todo/api/v1.0/hello
@app.route("/todo/api/v1.0/hello", methods=['GET'])
def hello():
    global hello_word
    tmp = request.args.get('word')
    if tmp:
        hello_word = tmp
    return "Hello " + hello_word + " !"

# curl 127.0.0.1:5000/todo/api/v1.0/sensors
@app.route('/todo/api/v1.0/sensors', methods=['GET'])
def get_sensor_readings():
    return jsonify({'batch': batch})
  
# curl 127.0.0.1:5000/todo/api/v1.0/battery_health
@app.route('/todo/api/v1.0/battery_health', methods=['GET'])
def get_battery_health():
    p = os.popen('cat /sys/class/power_supply/battery/health', "r")
    return(p.readline())

if __name__ == '__main__':
    app.run(debug=True)
