# -*- coding: utf-8 -*-

import rrdtool
import os


class Database(object):
    def __init__(self, filename):
        self.filename = filename
        self.create()

    def create(self):
        if not os.path.exists(self.filename):
            print 'create database: %s' % self.filename
            rrdtool.create(
                self.filename,
                '--step', '60',
                'DS:hum1:GAUGE:600:0:100',
                'DS:temp1:GAUGE:600:0:50',
                'RRA:MAX:0.5:1:288'
            )

    def update(self, humidity, temperature):
        rrdtool.update(self.filename, 'N:%s:%s' % (int(float(humidity)), int(float(temperature))))

    def graph(self):
        rrdtool.graph(
            'chac/static/temp.png', '--slope-mode', '--start', '-6h', '-w', '785', '-h', '120', u'--vertical-label=Température °C',
            'DEF:temp1=%s:temp1:MAX' % self.filename,
            'LINE:temp1#ff0000:"temp 1"'
        )
        rrdtool.graph(
            'chac/static/hum.png', '--slope-mode', '--start', '-6h', '-w', '785', '-h', '120',  u'--vertical-label=Humidité %',
            'DEF:hum1=%s:hum1:MAX' % self.filename,
            'LINE:hum1#00ff00:"hum 1"'
        )
