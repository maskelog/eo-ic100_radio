#!/usr/bin/env python

import time
import datetime
import struct
import rds
import besfm

'''
Get rds data from radio.
Use rdssurveyor -ingrouphexfile [filename] to read data
'''

try:
    fm = besfm.BesFM()
except:
    print("Device not found. Quitting.")
    quit()

rdsparse = rds.RDS()

fm.set_power(False)
fm.set_power(True)
fm.set_volume(0)
fm.set_rds(True) # Loud pop warning!
fm.set_channel(107.0)

fname = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.rdsgrouphex')
print(f'writing at {fname}')
f = open(fname, 'w')
while True:
    res = fm.get_status()
    if res['type'] == 'rds' and res['error'] == 0:
        rds = res['data'].hex()
        print(res)
        f.write(f"{rds[0:4]} {rds[4:8]} {rds[8:12]} {rds[12:16]} @{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')}\n")
    time.sleep(0.1)
