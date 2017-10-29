#!/usr/bin/env python3

try:
    from sense_hat import SenseHat
except:
    from sense_emu import SenseHat
    print("SenseHat emulator geimporteerd!")

import tempfile
import time
import random
import os


global stream, shutdown_counter, measure
(fileid, filename) = tempfile.mkstemp(suffix='.csv', prefix='acc_', dir=tempfile._os.getcwd()+'/data/')
print('Output gaat naar: %s'%(filename))
stream = open(filename, 'a')

start=50
stop=255
step=50

sense=SenseHat()
measure = False
rgb1=100
rgb2=100
rgb3=100
shutdown_counter = 0

def clamp(number, min_number=50, max_number=255):
    return min(max_number, max(min_number, value))

def adddata(number,add):
    add = abs(int(add))
    return clamp(number+add)

def randnumber(value):
    number = int(abs(value)*200+50)
    if number > 254:
        number =250
    return number

def start():
    sense.show_letter('R',text_colour=[255,0,0])

def pause():
    sense.show_letter('P', text_colour=[255,255,0])

def stop():
    sense.set_pixels([[0,0,0]]*64)

def shutdown():
    global stream,shutdown_counter
    if shutdown_counter == 0:
        stop()
        sense.show_letter('Q', text_colour=[0,255,0])
        shutdown_counter = 1
    elif shutdown_counter == 1:
        sense.show_letter('Q', text_colour=[0,0,255])
        shutdown_counter = 2
    elif shutdown_counter == 2:
        if not stream.closed:
            stream.close()
        stop()
        sense.set_pixel(7,7,10,10,10)
        time.sleep(0.5)
        os.system('sudo shutdown -h now')


def run_measurement():
    data=sense.get_accelerometer_raw()
    #rgb1=randnumber(data['x'])
    #rgb2=randnumber(data['y'])
    #rgb3=randnumber(data['z'])
    stream.write('%s,%s,%s,%s\n'%(time.time(), data['x'], data['y'], data['z']))

def startstop(event):
    global measure, filename, stream, shutdown_counter
    if event.action in ('pressed'):
        if event.direction is 'down':
            measure = False
            time.sleep(0.1)
            stop()
            if not stream.closed:
                stream.close()
            pause()
            shutdown_counter=0
        elif event.direction is 'up':
            if stream.closed:
                stream = open(filename,'a')
            start()
            measure = True
            shutdown_counter = 0
        elif event.direction is 'middle':
            shutdown()

measure = False
sense.stick.direction_any = startstop
while True:
    if measure:
        run_measurement()
    
