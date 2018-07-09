#!/usr/bin/env python3
# -*- coding: utf-8-*-
# author: Tiger
# SR501 interface & pin connection
# (1)(2)---NC
# (3)(4)---VCC
# (5)(6)---GND
# (7)(8)---DATA
# (9)(10)--NC

import RPi.GPIO as GPIO  
import time  

class SR501:

    def __init__(self):
        self.channel = 14
        self.RSSI = 0

    def init(self):
        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(self.channel, GPIO.IN)  

    def check_status(self):
        if GPIO.input(self.channel) == True:
            self.RSSI = 100
        else:
            self.RSSI = 0

    def close(self):
        GPIO.cleanup(self.channel)

if __name__ == "__main__":

    try:
        srdev = SR501()
        srdev.init()
        while True:
            srdev.check_status()
            if srdev.RSSI == 100:
                print("################## SR501 Alarm!!")
            elif srdev.RSSI == 0:
                print("SR501 Idle~ ****************")
            time.sleep(5)
    finally:
        srdev.close()
