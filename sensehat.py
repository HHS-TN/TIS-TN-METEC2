#!/usr/bin/env python3

import os,subprocess

# check if RTIMULib file is ok and copy file from #USB to usuable location
BASEPATH='/home/pi/TIS-TN-METR2-code/'
USBRTIMU=BASEPATH+'data/RTIMULib.ini'
RTIMUPATH='/home/pi/.config/sense_hat/RTIMULib.ini'
def copy(fh):
    p=subprocess.Popen('cp %s %s'%(fh,RTIMUPATH),stdout=subprocess.PIPE, shell=True)
    (output,err) = p.communicate()
    p_status = p.wait()
    print(p_status)

copy(BASEPATH+'RTIMULib.org')

# test if user is using own RTIMULib.ini file from USB-stick, and use the file
if (os.path.isfile(USBRTIMU)):
    print("USB-IMU")
    copy(USBRTIMU)


os.exit()

try:
    from sense_hat import SenseHat
except:
    from sense_emu import SenseHat
    print("SenseHat emulator geimporteerd!")

import tempfile
import time
import random

DEBUG=0 #no printing


def letter_colour(L,C):
    ''' Function to display a letter (L) with colour (C) on screen '''
    sense.show_letter(L,text_colour=C)

def reset_screen():
    sense.set_pixels([[0,0,0]]*64)

def shutdown():
    global stream,shutdown_counter
    if shutdown_counter == 0:
        reset_screen()
        letter_colour('Q', [0,255,0])
        shutdown_counter = 1
    elif shutdown_counter == 1:
        letter_colour('Q', [0,0,255])
        shutdown_counter = 2
    elif shutdown_counter == 2:
        if not stream.closed:
            stream.close()
        reset_screen()
        time.sleep(0.5)
        reset_screen()
        os.system('sudo shutdown -h now')


def run_measurement():
    data=sense.get_accelerometer_raw()
    stream.write('%s,%s,%s,%s\n'%(time.time(), data['x'], data['y'], data['z']))

def startstop(event):
    global measure, filename, stream, shutdown_counter
    if event.action in ('pressed'):
        if event.direction is 'down':
            measure = False
            time.sleep(0.1)
            reset_screen()
            if not stream.closed:
                stream.close()
            letter_colour('P', [0,255,0])
            shutdown_counter=0
        elif event.direction is 'up':
            if stream.closed:
                stream = open(filename,'a')
            letter_colour('R', [255,0,0])
            measure = True
            shutdown_counter = 0
        elif event.direction is 'left':
            letter_colour('%s'%(accel_range), [255,0,255])
        elif event.direction is 'middle':
            shutdown()

global stream, shutdown_counter, measure 
# create unique filename in ./data/
(fileid, filename) = tempfile.mkstemp(suffix='.csv', prefix='acc_', dir=BASEPATH+'data/')
if DEBUG:
    print('Output gaat naar: %s'%(filename))
stream = open(filename, 'a')

# initialise sensor and set start values for counters
sense=SenseHat()
reset_screen()
rtimulib_config = sense._get_settings_file('RTIMULib')
accel_range = rtimulib_config.LSM9DS1AccelFsr

measure = False
shutdown_counter = 0

# send joystick values to startstop function
sense.stick.direction_any = startstop

letter_colour('?', [30,255,30])

# start endless loop
while True:
    if measure:
        run_measurement()
    
