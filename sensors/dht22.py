import datetime
import time
import Adafruit_DHT

sensor = Adafruit_DHT.AM2302
pin = 23

class Sensor:
    def id(self):
        return "DHT22"

    def get_value(self):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return { "Time" : datetime.datetime.now().isoformat(),
                 "DHT22" : {
                     "Temperature" : round(temperature, 1),
                     "Humidity" : round(humidity, 1)
                 },
                 "TempUnit" : "C"
               }

    def templates(self, device_id, room):
        myid = self.id()
        return [{
            "name": "{} {} Temperature".format(room, myid),
            "uniq_id": "{}_{}_Temperature".format(device_id, myid),
            "unit_of_meas": "°C",
            "val_tpl": "{{value_json['DHT22'].Temperature}}",
            "dev_cla": "temperature"
        },{
            "name": "{} {} Humidity".format(room, myid),
            "uniq_id": "{}_{}_Humidity".format(device_id, myid),
            "unit_of_meas": "%",
            "val_tpl": "{{value_json['DHT22'].Humidity}}",
            "dev_cla": "humidity"
        }]
