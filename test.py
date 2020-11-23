#!/usr/bin/env python3.7

import subprocess
import json
import datetime
import time
import csv
from urllib.request import urlopen


"""Run iperf3 and log output to example.csv"""
def iperf_bash():
    subprocess.run(['iperf3', '-c', '192.168.1.130', '-t', '60', '--logfile', 'example.csv'])


"""Get weather in json file, pick out relevant data"""
def get_weather():
    with urlopen("http://wttr.in/Stavanger?format=j1") as response:
        source = response.read()
    data = json.loads(source)
    for item in data['current_condition']:
        temp = item['temp_C']
        pressure = item['pressure']
        cloudcover = item['cloudcover']
        weather = item['weatherDesc'][0]['value']
        print(temp, pressure, cloudcover, weather)
    return temp, pressure, cloudcover, weather


"""csv writer"""
def write_csv(data):
    with open('example.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


"""get time"""
def get_time():
    curr_time = datetime.datetime.now()
    curr_time = curr_time.strftime("%b %d %Y %H:%M:%S")
    print(curr_time)
    return [curr_time]


"""main loop"""
while True:
    write_csv(get_weather())
    write_csv(get_time())
    iperf_bash()
    time.sleep(3600)


