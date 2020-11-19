#!/usr/bin/env python3.7

import subprocess
import json
import datetime
import time
import iperf3
import requests
import csv
from urllib.request import urlopen
from subprocess import Popen, PIPE, STDOUT


def iperf_tester():
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = '127.0.0.1'
    client.port = 5201
    client.verbose = True
#    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()
#    print(result)
    print(' Megabits per second: {0}'.format(result.sent_Mbps))
    result_formatted = format(result.sent_Mbps)
    return [result_formatted]


def iperf_bash():
    subprocess.run(['iperf3', '-c', '127.0.0.1', '-t', '60', '--logfile', '>>', 'example.csv'])


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


def write_csv(data):
    with open('example.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


def get_time():
    curr_time = datetime.datetime.now()
    curr_time = curr_time.strftime("%b %d %Y %H:%M:%S")
    print(curr_time)
    return [curr_time]


while True:
    write_csv(get_weather())
    write_csv(get_time())
    iperf_bash()
#    iperf_tester()
#    write_csv(iperf_tester())
#    time.sleep(60)
#    i = 0
#    for i in range(0,60):
#        iperf_tester()
#        write_csv(iperf_tester())
#        i+=1


