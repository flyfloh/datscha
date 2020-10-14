""""
Read data from CO2 sensor
"""

import datetime
import time
import logging
import serial

MHZ19_SIZE = 9
MZH19_READ = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]

class Sensor:
    def id(self):
        return "MHZ19B"

    def get_value(self):
        ppm, t = self._read()
        myid = self.id()
        return { "Time" : datetime.datetime.now().isoformat(),
                 myid : {
                     "CarbonDioxide" : ppm,
                     "Temperature" : t
                 },
                 "TempUnit": "C"
               }

    def templates(self, device_id, room):
        myid = self.id()
        return [
            {
                "name": "{} {} Temperature".format(room, myid),
                "uniq_id": "{}_{}_Temperature".format(device_id, myid),
                "unit_of_meas": "°C",
                "val_tpl": "{{{{value_json['{}'].Temperature}}}}".format(myid),
                "dev_cla": "temperature"
            },
            {
                "name": "{} {} CarbonDioxide".format(room, myid),
                "uniq_id": "{}_{}_CarbonDioxide".format(device_id, myid),
                "unit_of_meas": " ",
                "val_tpl": "{{{{value_json['{}'].CarbonDioxide}}}}".format(myid),
            }]


    def __init__(self):
        self._serial_device = "/dev/ttyAMA0"

    def _read(self):
        """ Read the CO2 PPM concenration and temperature from a MH-Z19 sensor"""

        logger = logging.getLogger(__name__)

        ser = serial.Serial(port=self._serial_device,
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)

        sbuf = bytearray()
        starttime = time.time()
        finished = False
        timeout = 2
        res = None
        ser.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')
        while not finished:
            mytime = time.time()
            if mytime - starttime > timeout:
                logger.error("read timeout after %s seconds, read %s bytes",
                             timeout, len(sbuf))
                return None

            if ser.inWaiting() > 0:
                sbuf += ser.read(1)

                if len(sbuf) == MHZ19_SIZE:
                    # TODO: check checksum

                    res = (sbuf[2]*256 + sbuf[3], sbuf[4] - 40)
                    logger.debug("Finished reading data %s", sbuf)
                    finished = True

            else:
                time.sleep(.1)
                logger.debug("Serial waiting for data, buffer length=%s",
                             len(sbuf))

        return res
