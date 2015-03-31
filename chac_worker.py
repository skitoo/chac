# -*- coding: utf-8 -*-

import serial
import datetime
import logging

from chac.db import Database
from chac import settings


logger = logging.getLogger(__name__)


def main():
    logger.info('running chac worker...')
    ser = serial.Serial('/dev/ttyACM0', 9600)
    db = Database(settings.DATABASE_PATH)
    while True:
        data = ser.readline()
        if 'data:' in data:
            humidity, temperature = data.replace('data:', '').split('#')
            db.update(humidity, temperature)
            logger.info("update db: %s" % datetime.datetime.now())


if __name__ == '__main__':
    main()
