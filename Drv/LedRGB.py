#!/usr/bin/env python3
# -*- coding: utf-8-*-
# author: Tiger
# RGB LED module pin connection
# (1)(2)---NC
# (3)(4)---NC
# (5)(6)---GND
# (7)(8)---Red
# (9)(10)--Green
# (11)(12)--Blue

import RPi.GPIO as GPIO  
import time  

class LED:
	
    def __init__(self):
        self.RCHN = 14  
        self.GCHN = 15         
        self.BCHN = 18
         
    def init(self, CHR=14, CHG=15, CHB=18):
        self.RCHN = CHR
        self.GCHN = CHG
        self.BCHN = CHB    
        GPIO.setmode(GPIO.BCM)  
        time.sleep(0.1)                  
        GPIO.setup(self.RCHN, GPIO.OUT)  
        GPIO.setup(self.GCHN, GPIO.OUT) 
        GPIO.setup(self.BCHN, GPIO.OUT)                 
        GPIO.output(self.RCHN, GPIO.LOW)    
        GPIO.output(self.GCHN, GPIO.LOW) 
        GPIO.output(self.BCHN, GPIO.LOW) 
        
    def red_on(self):
	    GPIO.output(self.RCHN, GPIO.HIGH)  
	         
    def red_off(self):
	    GPIO.output(self.RCHN, GPIO.LOW) 
	    
    def green_on(self):
	    GPIO.output(self.GCHN, GPIO.HIGH)

    def green_off(self):
	    GPIO.output(self.GCHN, GPIO.LOW) 	    

    def blue_on(self):
	    GPIO.output(self.BCHN, GPIO.HIGH)	    

    def blue_off(self):
	    GPIO.output(self.BCHN, GPIO.LOW)

    def rgb_on(self):
	    GPIO.output(self.RCHN, GPIO.HIGH) 
	    GPIO.output(self.GCHN, GPIO.HIGH)	    	    
	    GPIO.output(self.BCHN, GPIO.HIGH)

    def rgb_off(self):
	    GPIO.output(self.RCHN, GPIO.LOW) 
	    GPIO.output(self.GCHN, GPIO.LOW)	    	    
	    GPIO.output(self.BCHN, GPIO.LOW)

    def close(self):
        GPIO.cleanup(self.RCHN)
        GPIO.cleanup(self.GCHN)
        GPIO.cleanup(self.BCHN)
	    	    	 
if __name__ == "__main__":

    try:	
        led = LED()
        led.init()
        while True:
            led.green_on()
            time.sleep(1)
            led.green_off()
            time.sleep(1)
    finally:
	    led.close()      