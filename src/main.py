from pyroute2 import IPDB
from flask import Flask
import os
ipdb = IPDB()

myname = os.getenv('RESIN_DEVICE_NAME_AT_INIT')

def set_ipaddress_eth0(ipaddress):
    with ipdb.interfaces.eth0 as eth0:
        eth0.add_ip(str(ipaddress)+'/24')
        print('Setting eth0 ipaddress to '+str(ipaddress))

def set_ipaddress_wlan0(ipaddress):
    with ipdb.interfaces.wlan0 as wlan0:
        wlan0.add_ip(str(ipaddress)+'/24')
        print('Setting wlan0 ipaddress to '+str(ipaddress))
        


if myname == 'Server_C1':
    set_ipaddress_eth0('192.168.88.230')
    set_ipaddress_wlan0('10.0.10.230')
    
elif myname == 'Client_C1':
    set_ipaddress_eth0('192.168.88.231')
    set_ipaddress_wlan0('10.0.10.231') 

elif myname == 'Server_C2':
    set_ipaddress_eth0('192.168.88.232')
    set_ipaddress_wlan0('10.0.10.232')

elif myname == 'Client_C2':
    set_ipaddress_eth0('192.168.88.233')
    set_ipaddress_wlan0('10.0.10.233')
    
elif myname == 'Server_C3':
    set_ipaddress_eth0('192.168.88.234')
    set_ipaddress_wlan0('10.0.10.234')

elif myname == 'Client_C3_1':
    set_ipaddress_eth0('192.168.88.235')
    set_ipaddress_wlan0('10.0.10.235')
    
elif myname == 'Client_C3_2':
    set_ipaddress_eth0('192.168.88.236')
    set_ipaddress_wlan0('10.0.10.236')   
    
elif myname == 'Client_C9':
    set_ipaddress_eth0('192.168.88.237')
    set_ipaddress_wlan0('10.0.10.237')    

elif myname == 'RPI hjemme hos HHH':
    set_ipaddress_eth0('192.168.1.238')
    #set_ipaddress_wlan0('10.0.10.237')    
    
else
    print('Devicename not found, ipaddress not set')



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Matrix Ethernet Tester Version 0.1'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)