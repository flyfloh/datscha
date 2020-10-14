#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import device
import mqtt as comm
import config
import importlib

def load_sensors(cfg):
    sensors = []
    for sensor in cfg.get("sensors"):
        module_name = "sensors.{}".format(sensor)
        module = importlib.import_module(module_name)
        class_ = getattr(module, "Sensor")
        sensors.append(class_())
    return sensors

def init(cfg, channel):
    dev = device.Device(cfg.get("room"))

    sensors = load_sensors(cfg)
    for s in sensors:
        room = cfg.get("room")
        channel.sensor_init(sensor_id=s.id(),
                device=dev.template(),
                templates=s.templates(dev.id(), room),
                room=room)

    return sensors

def telemetry_loop(sensors, channel, room, telemetry_time):
    while True:
        for s in sensors:
            channel.send_telemetry(sensor_id=s.id(),
                    room=room,
                    payload=s.get_value())
        time.sleep(telemetry_time)

if __name__ == "__main__":
    cfg = config.Config()
    channel = comm.Channel(cfg.get("host"))
    sensors = init(cfg, channel)
    telemetry_loop(sensors, channel, cfg.get("room"), cfg.get("telemetry_time"))
