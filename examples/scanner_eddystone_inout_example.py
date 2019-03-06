import time
from beacontools import BeaconScanner, EddystoneTLMFrame, EddystoneFilter, EddystoneUIDFrame
bt_list={}

def callback(bt_addr, rssi, packet, additional_info):
#    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))
    id="namespace:"+additional_info["namespace"]+" Instance:"+additional_info["instance"]
    if not (id in bt_list):
        print("<IN> %s " % (id))
    currentCPUTime=time.perf_counter()
    bt_list[id]=currentCPUTime
    
# scan for all TLM frames of beacons in the namespace "12345678901234678901"
scanner = BeaconScanner(callback, 
    device_filter=EddystoneFilter(namespace="12345678901234678901"),
    packet_filter=[EddystoneTLMFrame, EddystoneUIDFrame]
)
scanner.start()

try:
    while True:
        for i in list(bt_list):
            print("<Listing> %s %d" % (i,time.perf_counter()-bt_list[i]))
            #Wait 30s for detecting to exit beacon.
            if(time.perf_counter()-bt_list[i]>30):
                print("<OUT> %s " % (i))
                del bt_list[i]
            else:
                print("<Listing> %s %d" % (i,time.perf_counter()-bt_list[i]))
        time.sleep(1)
except KeyboardInterrupt:
    scanner.stop()