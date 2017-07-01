try:
    from sense_hat import SenseHat
except:
    from sense_emu import SenseHat
    print("SenseHat emulator geimporteerd!")

import tempfile
import time
import random
import os


global file
global stream
(file, filename) = tempfile.mkstemp(suffix='.csv', prefix='acc_', dir=tempfile._os.getcwd())
print('Output gaat naar: %s'%(filename))
stream = open(file, 'a')

start=50
stop=255
step=50

sense=SenseHat()
global measure
measure = False
rgb1=100
rgb2=100
rgb3=100

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
    sense.show_letter('S',text_colour=[255,0,0])

def stop():
    sense.set_pixels([[0,0,0]]*64)

def run_measurement():
    data=sense.get_accelerometer_raw()
    rgb1=randnumber(data['x'])
    rgb2=randnumber(data['y'])
    rgb3=randnumber(data['z'])
    stream.write('%s,%s,%s,%s\n'%(time.time(), data['x'], data['y'], data['z']))

def startstop(event):
    global measure, file, stream
    if event.action in ('pressed'):
        if event.direction is 'down':
            measure = False
            time.sleep(0.1)
            stop()
            if not stream.closed:
                stream.close()
        elif event.direction is 'up':
            if stream.closed:
                stream = open(filename,'a')
            start()
            measure = True

measure = False
sense.stick.direction_up = startstop
sense.stick.direction_down = startstop

while True:
    if measure:
        run_measurement()
    
