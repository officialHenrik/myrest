#!/usr/bin/env python3

from flask import Flask, jsonify
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

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/todo/api/v1.0/sensors', methods=['GET'])
def get_sensor_readings():
    return jsonify({'batch': batch})

@app.route('/todo/api/v1.0/battery_health', methods=['GET'])
def get_battery_health():
    p = os.popen('cat /sys/class/power_supply/battery/health', "r")
    return(p.readline())

if __name__ == '__main__':
    app.run(debug=True)
