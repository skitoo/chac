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
                'DS:temp1:GAUGE:600:-50:50',
                'DS:hum2:GAUGE:600:0:100',
                'DS:temp2:GAUGE:600:-50:50',

                # every minute during 1 month
                'RRA:MAX:0.5:1:44640',
                'RRA:MIN:0.5:1:44640',
                'RRA:AVERAGE:0.5:1:44640',

                # every hour during 1 year
                'RRA:MAX:0.5:60:8760',
                'RRA:MIN:0.5:60:8760',
                'RRA:AVERAGE:0.5:60:8760',

                # every day during 100 years
                'RRA:MAX:0.5:86400:36500',
                'RRA:MIN:0.5:86400:36500',
                'RRA:AVERAGE:0.5:86400:36500',
            )

    def update(self, hum1, temp1, hum2=0, temp2=0):
        rrdtool.update(self.filename, 'N:%s:%s:%s:%s' % (hum1, temp1, hum2, temp2))

    def graph(self):
        rrdtool.graph(
            'chac/static/temp.png', '--slope-mode', '--start', '-6h', '-w', '785', '-h', '120', u'--vertical-label=Température °C',
            'DEF:temp1=%s:temp1:MAX' % self.filename,
            'DEF:temp2=%s:temp1:MIN' % self.filename,
            'DEF:temp3=%s:temp1:AVERAGE' % self.filename,
            'LINE:temp1#ff0000:"Max"',
            'LINE:temp2#00ff00:"Min"',
            'LINE:temp3#0000ff:"Average"'
        )
        rrdtool.graph(
            'chac/static/hum.png', '--slope-mode', '--start', '-6h', '-w', '785', '-h', '120',  u'--vertical-label=Humidité %',
            'DEF:hum1=%s:hum1:MAX' % self.filename,
            'DEF:hum2=%s:hum1:MIN' % self.filename,
            'DEF:hum3=%s:hum1:AVERAGE' % self.filename,
            'LINE:hum1#ff0000:"Max"',
            'LINE:hum2#00ff00:"Min"',
            'LINE:hum3#0000ff:"Average"'
        )
        rrdtool.graph(
            'chac/static/temp-day.png', '--slope-mode', '--start', '-1d', '-w', '785', '-h', '120', u'--vertical-label=Température °C',
            'DEF:temp1=%s:temp1:MAX' % self.filename,
            'LINE:temp1#ff0000:"temp 1"'
        )
        rrdtool.graph(
            'chac/static/hum-day.png', '--slope-mode', '--start', '-1d', '-w', '785', '-h', '120',  u'--vertical-label=Humidité %',
            'DEF:hum1=%s:hum1:MAX' % self.filename,
            'LINE:hum1#00ff00:"hum 1"'
        )
