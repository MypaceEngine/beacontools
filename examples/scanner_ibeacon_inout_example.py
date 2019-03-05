import time
from beacontools import BeaconScanner, IBeaconFilter
bt_list={}

def callback(bt_addr, rssi, packet, additional_info):
#    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    id="UUID:"+additional_info["uuid"]+" Major:"+str(additional_info["major"])+" Minor:"+str(additional_info["minor"])
    
    if not (id in bt_list):
        print("<IN> %s " % (id))
    currentCPUTime=time.perf_counter()
    bt_list[id]=currentCPUTime

# scan for all iBeacon advertisements from beacons with the specified uuid 
scanner = BeaconScanner(callback, 
    device_filter=IBeaconFilter(uuid="e5b9e3a6-27e2-4c36-a257-7698da5fc140")
)
scanner.start()

try:
    while True:
        for i in list(bt_list):
            print("<Listing> %s Timeout:%d" % (i,time.perf_counter()-bt_list[i]))
            #Wait 30s for detecting to exit beacon.
            if(time.perf_counter()-bt_list[i]>30):
                print("<OUT> %s " % (i))
                del bt_list[i]
        time.sleep(0.1)
except KeyboardInterrupt:
    scanner.stop()