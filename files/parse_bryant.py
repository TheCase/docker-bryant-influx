#!/usr/bin/env python

import sys, os
import urllib
import xmltodict
import json
from influxdb import InfluxDBClient
from pprint import pprint

zone_outs = ['fan','rt','rh','htsp','clsp']

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

def influx( names, value):
    tags = {}
    client = InfluxDBClient(os.environ['INFLUXHOST'], os.environ['INFLUXPORT'], os.environ['INFLUXUSER'], os.environ['INFLUXPASS'], os.environ['INFLUXDB'])
    parts = names.split('.') 
    measurement = parts[0]
    if measurement == 'operation':
    	tags['type'] = parts[1] 
    	tags['mode'] = parts[2]
    else:
    	tags['location'] = parts[1]
    if measurement == 'target':
    	tags['type'] = parts[2]
    if isNumber(value):
	value = float(value)
    data = [ 
         { 
           "measurement": str(measurement), 
           "tags": tags, 
           "fields": { "value": value }
         }
    ]
    client.write_points(data)

def stats_write ( data ):
    print ' mark ===='
    for key,val in data.iteritems():
        print key + ': ' + str(val)
        influx(key, val)

def parse(string):
    modded = string.replace('data=','')
    xml = urllib.unquote(modded)
    try:
        data = xmltodict.parse(xml)
    except:
        print 'no data, move along...'
    else:
        if 'status' in data:
            process(data['status'])
        else:
            print 'not status data, move along...'

def binaryState(s):
    state = 0
    if s == 'on':
      state = 1
    return state

def process(status):
    output = {}
    state = binaryState(status['humid'])
    output.update({'operation.humidity.'+ status['humid']: state})
    output.update({'operation.temperature.'+status['mode']: 1})
    output.update({'temperature.outdoor': status['oat']})
 
    for zone in status['zones']['zone']:
        if zone['enabled'] == 'on':
            name = zone['name']
            state = binaryState(zone['fan'])
	    output.update({'fan.'+name: state})
	    output.update({'humidity.'+name: zone['rh']})
	    output.update({'temperature.'+name: zone['rt']})
	    output.update({'target.'+name+'.heat': zone['htsp']})
	    output.update({'target.'+name+'.cool': zone['clsp']})
    stats_write(output)
            

