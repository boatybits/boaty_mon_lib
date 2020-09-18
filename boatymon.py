import network
from machine import Pin, I2C
import ujson
import utime


class sensors:
    def __init__(self):
        with open("config.py") as json_data_file:
            self.conf = ujson.load(json_data_file)
        self.led = Pin(2, Pin.OUT)      # internal led is on pin 2
        self.station = network.WLAN(network.STA_IF)
        print('new sensors instance created')

    def connectWifi(self):
        self.station.active(True)
        print('\n', 'station.active = ', self.station.active(), '\n')
        networks = self.station.scan()
        print('\n', '****** No. of networks = ', len(networks), '\n')
        print('***** networks = ', networks, '\n')

        if not self.station.isconnected():
            print('***** Connecting to network...')
            try:
                self.station.ifconfig((self.conf['ESP_IP_Address'],
                                       '255.255.255.0', '10.10.10.1',
                                       '10.10.10.1'))
                self.station.connect(self.conf['ssid'], self.conf['password'])
                self.udpAddr = self.conf['udp_IP_Addr']
            except Exception as e:
                print('***** connect wifi failure, error =', e, "\nRetrying")
                pass

            counter = 0
            while not self.station.isconnected():
                utime.sleep(0.25)
                print("\r>", counter, end='')
                counter += 1
                self.flashLed()
                if counter > 100:
                    machine.reset()
                pass
        print('\n', '***** CONNECTED!! network config:',
              self.station.isconnected(), '\n', self.station.ifconfig(), '\n')

    def flashLed(self):
        self.led.value(not self.led.value())

    def slow_loop(self):  # which sensors to send, triggered by usynchio
        if not self.station.isconnected():
            print("***** Reconnecting from slow loop")
            self.connectWifi()

        self.flashLed()
