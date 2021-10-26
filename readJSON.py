import json
import os

#get data in Mbit/s sent
def data_sent():
    return float((data['end']['sum_sent']['bits_per_second']))/1048576
#get data in Mbit/s received
def data_received():
    received = float((data['end']['sum_received']['bits_per_second']))/1048576
    return received

filesize = os.path.getsize("/home/innova/results.json")

if filesize == 0:
    print("Results are not ready")
else:
    fp = open("/home/innova/results.json")
    data = json.load(fp)
    if "error" in data: #check if there is an error in json data
        print (data['error'])
    else: #print datarates   
        data_sent = (data_sent())
        data_sent = int(data_sent)
        print ("Sending datarate: " + str(data_sent) + " Mbit/s" )
        data_received = (data_received())
        data_received = int(data_received)
        print ("Receiving datarate: " + str(data_received) + " Mbit/s" )



