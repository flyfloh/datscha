#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sensors.ds18b20 as ds18b20
import sensors.mhz19 as mhz19
import mqtt as comm

#mqtt_host = "mqtt.hm.halbmastwurf.de"
cfg = {
  "room" : "livingroom",
  "telemetry_time" : 60,
  "host" : "192.168.56.2"
}


def init(channel):
    sensors = [
      ds18b20.Sensor(),
      mhz19.Sensor()
    ]

    for s in sensors:
        room = cfg["room"]
        channel.sensor_init(sensor_id=s.id(),templates=s.templates(room), room=room)

    return sensors

def telemetry_loop(sensors, channel):
    while True:
        for s in sensors:
            channel.send_telemetry(sensor_id=s.id(),room=cfg["room"],payload=s.get_value())
        time.sleep(cfg["telemetry_time"])

if __name__ == "__main__":
    channel = comm.Channel(cfg["host"])
    sensors = init(channel)
    telemetry_loop(sensors, channel)
