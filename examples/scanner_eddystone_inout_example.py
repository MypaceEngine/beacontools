import time
from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter, EddystoneUIDFrame
bt_list={}

def callback(bt_addr, rssi, packet, additional_info):
#    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    id="namespace:"+additional_info["namespace"]+" Instance:"+additional_info["instance"]
    print("<Receive> %s " % (id))
    if not (id in bt_list):
        print("<IN> %s " % (id))
    currentCPUTime=time.perf_counter()
    bt_list[id]=currentCPUTime
    
scanner=None
scannerStartTime=0;

try:
    while True:
        if(scanner==None)or(time.perf_counter()-scannerStartTime>3600):
            print("<Beacon Scanner Restart>")
            if not (scanner==None):
                scanner.stop()
            # scan for all TLM frames of beacons in the namespace "01020304050607080910"
            scanner = BeaconScanner(callback, 
                device_filter=EddystoneFilter(namespace="01020304050607080910"),
                packet_filter=[EddystoneTLMFrame, EddystoneUIDFrame]
            )
            scanner.start()
            scannerStartTime=time.perf_counter()
        for i in list(bt_list):
            #Wait 30s for detecting to exit beacon.
            if(time.perf_counter()-bt_list[i]>30):
                print("<OUT> %s " % (i))
                del bt_list[i]
            else:
                print("<Listing> %s %d" % (i,time.perf_counter()-bt_list[i]))
        time.sleep(1)
except KeyboardInterrupt:
    scanner.stop()