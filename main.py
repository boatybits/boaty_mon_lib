#!/usr/bin/env python3
import uasyncio
import esp32
import boatymon

mySensors = boatymon.sensors()
mySensors.connectWifi()

loop = uasyncio.get_event_loop()

timer=0
async def slow_loop():
    global timer
    while True:      
        mySensors.slow_loop()
        await uasyncio.sleep(1)

async def fast_loop():
    while True:
        #mySensors.dataBasesend()
        await uasyncio.sleep_ms(200)
        
    
# async def call_mqtt():
#     while True:
#         try:
#             client.check_msg()
#         except Exception as e:
#             print("mqtt connect error from call_mqtt function, main line 36. error = ",e)
#             mySensors.connectWifi()
#             pass
#         await uasyncio.sleep_ms(500)

# loop.create_task(call_mqtt())
loop.create_task(slow_loop())
loop.create_task(fast_loop())
# loop.create_task(read_UART())
loop.run_forever()