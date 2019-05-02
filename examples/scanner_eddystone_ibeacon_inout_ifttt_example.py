import time
import datetime
import sys
import json
import urllib.request
from datetime import datetime

from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter, EddystoneUIDFrame, BeaconScanner, IBeaconFilter
bt_list={}

def callback(bt_addr, rssi, packet, additional_info):
    try:
        id="Type:Unkonown Adress:"+bt_addr
        if("namespace" in additional_info):
            id="Type:Eddystone Adress:"+bt_addr+" Namespace:"+additional_info["namespace"]+" Instance:"+additional_info["instance"]
        elif("uuid" in additional_info):
            id="Type:iBeacon Adress:"+bt_addr+" UUID:"+additional_info["uuid"]+" Major:"+str(additional_info["major"])+" Minor:"+str(additional_info["minor"])
        print("<Receive> %s " % (id))
        if not (id in bt_list):
            print("<IN> %s " % (id))
            sendIFTTT({ 'value1' : datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'value2' : 'BEACON IN', 'value3' : id})
        currentCPUTime=time.perf_counter()
        bt_list[id]=currentCPUTime
    except:
        print(sys.exc_info())

def sendIFTTT(data):
    url = 'https://maker.ifttt.com/trigger/<Your Event Name>/with/key/<Your key>'
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
    
# scan for all TLM frames of beacons
scanner = BeaconScanner(callback)
scanner.start()

try:
    while True:
        if(len(bt_list)==0):
            print("<No Listing>")
        for i in list(bt_list):
            #Wait 30s for detecting to exit beacon.
            if(time.perf_counter()-bt_list[i]>30):
                print("<OUT> %s " % (i))
                sendIFTTT({ 'value1' : datetime.now().strftime("%Y/%m/%d %H:%M:%S"), 'value2' : 'BEACON OUT', 'value3' : i})
                del bt_list[i]
            else:
                print("<Listing> %s %d" % (i,time.perf_counter()-bt_list[i]))
        time.sleep(1)
except KeyboardInterrupt:
    scanner.stop()