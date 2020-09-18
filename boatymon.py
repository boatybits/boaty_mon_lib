import network
from machine import Pin, I2C
import ujson
import utime

class sensors:
    def __init__(self):
        
        with open("config.py") as json_data_file:
            self.conf = ujson.load(json_data_file)
        
        self.led = Pin(2, Pin.OUT)      #internal led is on pin 2  
            
        print('new sensors instance created')
        
    def connectWifi(self):        
        
        sta_if = network.WLAN(network.STA_IF)
        print('\n', 'sta_if.active = ', sta_if.active(), '\n')
        sta_if.active(True)
        print('\n', 'sta_if.active = ', sta_if.active(), '\n')
        networks = sta_if.scan()

        if not sta_if.isconnected():
            print('        connecting to network...')
            
            print('\n','        No. of networks = ', len(networks), '\n')
            print('        networks = ', networks, '\n')
            try:
                sta_if.ifconfig((self.conf['IP_Address'], '255.255.255.0', '10.10.10.1', '10.10.10.1'))
                sta_if.connect(self.conf['ssid'], self.conf['password'])
                self.udpAddr = '10.10.10.1'
            except Exception as e:
                print('connect wifi failure, error =',e)
                pass
                
            counter = 0
            while not sta_if.isconnected():
                utime.sleep(0.25)
                print("\r>", counter, end = '')
                counter += 1
                self.flashLed()
                if counter > 100:
                    machine.reset()
                pass
        print('\n', '    CONNECTED!! network config:',sta_if.isconnected(),'\n', sta_if.ifconfig(), '\n')
        
    def flashLed(self):
        self.led.value(not self.led.value())
        
    def slow_loop(self):  #which sensors to send, triggered by usynchio
        self.flashLed()