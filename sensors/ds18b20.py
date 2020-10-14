#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import glob
import time

class Sensor:
    def id(self):
        return "DS18B20"

    def get_value(self):
        c, f = self._read_temp()
        return { "Time" : datetime.datetime.now().isoformat(),
                 "DS18B20" : { "Temperature" : c },
                 "TempUnit" : "C"
               }

    def templates(self, device_id, room):
        myid = self.id()
        return [{
            "name": "{} {}".format(room, myid),
            "uniq_id": "{}_{}".format(device_id, myid),
            "unit_of_meas": "°C",
            "val_tpl": "{{value_json['DS18B20'].Temperature}}",
            "dev_cla": "temperature"
        }]

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def _read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_temp(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
