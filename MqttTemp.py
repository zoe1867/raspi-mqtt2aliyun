#!/usr/bin/python3
# coding=utf-8

import datetime
import time
import hmac
import hashlib
import math
import json
#import LedRGB
import DH11
import SR501



dh11 = DH11.DH11()
dh11.init()
sr501 = SR501.SR501()
sr501.init()

TEST = 0

ProductKey = "pkey"
ClientId = "cid"  
DeviceName = "deviname"
DeviceSecret = "Dsec"

# signmethod
signmethod = "hmacsha1"
# signmethod = "hmacmd5"


us = math.modf(time.time())[0]
ms = int(round(us * 1000))
timestamp = str(ms)

data = "".join(("clientId", ClientId, "deviceName", DeviceName,
                "productKey", ProductKey, "timestamp", timestamp
                ))

print("data:", data)

if "hmacsha1" == signmethod:
    ret = hmac.new(bytes(DeviceSecret, encoding="utf-8"),
                   bytes(data, encoding="utf-8"),
                   hashlib.sha1).hexdigest()
elif "hmacmd5" == signmethod:
    ret = hmac.new(bytes(DeviceSecret, encoding="utf-8"),
                   bytes(data, encoding="utf-8"),
                   hashlib.md5).hexdigest()
else:
    raise ValueError

sign = ret
print("sign:", sign)

# ======================================================

strBroker = ProductKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
port = 1883

client_id = "".join((ClientId,
                     "|securemode=3",
                     ",signmethod=", signmethod,
                     ",timestamp=", timestamp,
                     "|"))
username = "".join((DeviceName, "&", ProductKey))
password = sign

print("="*30)
print("client_id:", client_id)
print("username:", username)
print("password:", password)
print("="*30)

def secret_test():
    DeviceSecret = "secret"
    data = "clientId12345deviceNamedeviceproductKeypktimestamp789"
    ret = hmac.new(bytes(DeviceSecret, encoding="utf-8"),
                   bytes(data, encoding="utf-8"),
                   hashlib.sha1).hexdigest()
    print("test:", ret)


# ======================================================
# MQTT Initialize.--------------------------------------

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("MQTT client not find. Please install as follow:")
    print("pip install paho-mqtt")


# ======================================================
def on_connect(mqttc, obj, rc,ls):
    print("OnConnetc, rc: " + str(rc))

    mqttc.subscribe("/sys/a1JB2i7MDAC/eUeoaRna3mjKUA20yw8S/thing/service/property/set", 0)


def on_publish(mqttc, obj, mid):
    print("OnPublish, mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print("Log:" + string)


def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    print(strcurtime + ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    on_exec(str(msg.payload))
    strply = str(msg.payload)[2:-1]
    print(strply)
    #GPIO = LedRGB.LED()
    #GPIO.init()
    dply = json.loads(strply)
    para = dply["params"]
    if "PowerSwitch" in para:
        if para["PowerSwitch"] == 1:
            print("Turn on led")
            #GPIO.RGB_ON()
        elif para["PowerSwitch"] == 0:
            print("Turn off led")
            #GPIO.RGB_OFF()
    

def on_exec(strcmd):
    print("Exec:", strcmd)
    strExec = strcmd


# =====================================================
if __name__ == '__main__':
    if TEST:
        secret_test()
        exit(0)

    mqttc = mqtt.Client(client_id)
    mqttc.username_pw_set(username, password)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    mqttc.connect(strBroker, port, 120)
    #mqttc.loop_forever()
    mqttc.loop_start()


    
    dh11.get_temp()
    data = {
    "id" : "789",
    "version":"1.0",
    "params" : {
        "IndoorTemperature":dh11.temperature,
        "CurrentHumidity":dh11.humidity,
        "RSSI":sr501.RSSI,
        "LightSwitch":1
    },
    "method":"thing.event.property.post"}
    dtstr = json.dumps(data)
    print(dtstr)
    #led = LedRGB.LED()
    #led.init()
    temp = 24
    hum = 50
    try:
        while True:
            mqttc.publish("/sys/a1JB2i7MDAC/eUeoaRna3mjKUA20yw8S/thing/event/property/post",dtstr)
            time.sleep(5.0)
            dh11.get_temp()
            sr501.check_status()
            print("******temperature:   %d"%dh11.temperature)
            print("******humidity:      %d"%dh11.humidity)
            print("******RSSI:          %d"%sr501.RSSI)
            if dh11.temperature !=0:
                temp = dh11.temperature
            if dh11.humidity !=0:
                hum = dh11.humidity
            data = {
            "id" : "789",
            "version":"1.0",
            "params" : {
                "IndoorTemperature":temp,
                "CurrentHumidity":hum,
                "RSSI":sr501.RSSI,
                "LightSwitch":1
            },
            "method":"thing.event.property.post"}
            dtstr = json.dumps(data)            
    except KeyboardInterrupt:
        pass 
    finally:
        pass
        #led.close()
