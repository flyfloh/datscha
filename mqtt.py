#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json

class Channel:
    def __init__(self, mqtt_host):
        self.client = mqtt.Client()
        try:
            self.client.connect(mqtt_host)
        except:
            print("Error connecting to MQTT host: {}".format(mqtt_host))
            print(sys.exc_info())
        self.client.loop_start()

    def sensor_init(self, sensor_id, device, templates, room):
        for t in templates:
            d = { "device" : device }
            topic, payload = self._discovery_msg(sensor_id, {**t, **d}, room)
            self._send(topic, json.dumps(payload), retain=True)

            topic, payload = self._online_msg(sensor_id, room)
            self._send(topic, payload, retain=True)

    def __del__(self):
        #topic, payload = self._offline_msg(sensor_id, room)
        #self._send(topic, payload, retain=True)
        self.client.disconnect()

    def _send(self, topic, payload, retain=False):
        print(topic)
        print(payload)
        self.client.publish(topic, payload, retain=retain)

    def _topics(self, sensor_id, room):
        base_topic = "{}_{}/tele".format(room, sensor_id)
        return {
                 "~" : base_topic,
                 "stat_t" : "{}/SENSOR".format(base_topic),
                 "avty_t" : "{}/LWT".format(base_topic)
               }

    def _offline_msg(self, sensor_id, room):
        topic = self._topics(sensor_id, room)["avty_t"]
        payload = "Offline"
        return topic, payload

    def _online_msg(self, sensor_id, room):
        topic = self._topics(sensor_id, room)["avty_t"]
        payload = "Online"
        return topic, payload

    def _discovery_msg(self, sensor_id, template, room):
        name = template["name"].replace(" ", "_")
        topic = "homeassistant/sensor/{}/config".format(name)
        sensor_topics = self._topics(sensor_id, room)
        mqtt_payload = {
            "pl_avail": "Online",
            "pl_not_avail": "Offline",
            # "json_attributes_topic": "~HASS_STATE",
            #"val_tpl": "{{value_json['RSSI']}}",
        }
        return topic, { **sensor_topics, **mqtt_payload, **template }

    def send_telemetry(self, sensor_id, room, payload):
        self._send(self._topics(sensor_id, room)["stat_t"], json.dumps(payload))
