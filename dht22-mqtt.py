import time

import Adafruit_DHT
import paho.mqtt.publish as publish

sensor = Adafruit_DHT.AM2302
pin = 23
mqtt_host = "192.168.56.81"

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print("Temp: {} Humidity: {}".format(temperature, humidity))
    try:
        publish.single("sensors/kitchen/temperature", temperature, hostname=mqtt_host)
        publish.single("sensors/kitchen/humidity", humidity, hostname=mqtt_host)
    except:
        print("Error connecting to mqtt host: {}".format(mqtt_host))

    time.sleep(60)

