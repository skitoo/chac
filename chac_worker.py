# -*- coding: utf-8 -*-

import serial
import datetime
import logging

from chac.db import Database
from chac import settings


logger = logging.getLogger(__name__)


def main():
    print('running chac worker...')
    ser = serial.Serial(settings.SERIAL_PORT, settings.SERIAL_BAUDRATE)
    db = Database(settings.DATABASE_PATH)
    while True:
        data = ser.readline()
        if 'data:' in data:
            humidity, temperature = map(float, data.replace('data:', '').split('#'))
            db.update(humidity, temperature)
            print("[%s] update - %s °C - %s %%" % (datetime.datetime.now(), temperature, humidity))


if __name__ == '__main__':
    main()
