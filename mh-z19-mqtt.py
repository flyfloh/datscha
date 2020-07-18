""""
Read data from CO2 sensor
"""

import time
import logging

import serial
import paho.mqtt.publish as publish

MHZ19_SIZE = 9
MZH19_READ = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]

def read_mh_z19(serial_device):
    """ Read the CO2 PPM concenration from a MH-Z19 sensor"""

    result = read_mh_z19_with_temperature(serial_device)
    if result is None:
        return None
    ppm, temp = result
    return ppm


def read_mh_z19_with_temperature(serial_device):
    """ Read the CO2 PPM concenration and temperature from a MH-Z19 sensor"""

    logger = logging.getLogger(__name__)

    ser = serial.Serial(port=serial_device,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)

    sbuf = bytearray()
    starttime = time.time()
    finished = False
    timeout = 2
    res = None
    ser.write("\xff\x01\x86\x00\x00\x00\x00\x00\x79")
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

if __name__ == '__main__':
    logging.info("Starting logger...")
    while True:
        ppm = read_mh_z19("/dev/ttyAMA0")
        print("CO2 concentration is {} ppm".format(ppm))
        publish.single("sensors/livingroom/co2", ppm, hostname="localhost")
        time.sleep(10)

