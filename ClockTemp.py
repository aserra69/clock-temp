#!/usr/bin/python

import math
import time
import datetime
import tty,sys          #for keyboard input detection
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

#Import BMP for measurement
import Adafruit_BMP.BMP085 as BMP085 

# Import for display
from Adafruit_LED_Backpack import SevenSegment

# Initialize I2C devices
segmentDisplay = SevenSegment.SevenSegment(address=0x70)  #Display
sensorTemp = BMP085.BMP085()   # Temp Sensor

# Initialize Input Devices
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(16, GPIO.OUT) # Set on board LED as an output

segmentDisplay.begin()   # Initialize the display. Must be called once before using the display.
GPIO.output(16, GPIO.LOW)   # Initialize on-board LED.  turning it off



def restart():  # to properly shutdown pi 
    # command = "/usr/bin/sudo /sbin/shutdown -r now"  # for shutdown and restart
    command = "/usr/bin/sudo /sbin/shutdown -h now"  # for halt and shutdown for power removal
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def displaywait():  # hold display then clear for next activity
    time.sleep(3)
    segmentDisplay.clear()

def buttoncheck():  # check to see if button has been pressed to shut down pi
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")
        segmentDisplay.clear()
        segmentDisplay.write_display()
        time.sleep(2)
        restart()

def timedisplay(): # To display the time
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    # Set hours
    segmentDisplay.set_digit(0, int(hour / 10))     # Tens
    segmentDisplay.set_digit(1, hour % 10)          # Ones
    # Set minutes
    segmentDisplay.set_digit(2, int(minute / 10))   # Tens
    segmentDisplay.set_digit(3, minute % 10)        # Ones
    # Toggle colon
    segmentDisplay.set_colon(True)                  # Toggle colon

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segmentDisplay.write_display()
    displaywait()
    
def tempdisplay(temprun): # display temperature
      if temprun == 1:  # run for Celcius	
       celciusRAW = sensorTemp.read_temperature()
       celciusTens = int (math.trunc(celciusRAW) / 10)
       celciusOnes = math.trunc(celciusRAW) % 10
       celciusFractional = int ((celciusRAW - math.trunc(celciusRAW)) * 10)
       print('Temp = {0:0.2f} *C'.format(sensorTemp.read_temperature()))
       # Set temperature display celcius
       segmentDisplay.set_digit(0, celciusTens)          # Tens
       segmentDisplay.set_digit(1, celciusOnes)          # Ones
       segmentDisplay.set_decimal(1, True)               # Set decimal point
       segmentDisplay.set_digit(2, celciusFractional)    # Tenths
       segmentDisplay.set_digit(3, 'C')                  # Celcius unit
       segmentDisplay.write_display()        # write to the display
       displaywait()
    
      if temprun == 2:  # run for fahrenheit
       fahrenheitRAW = (1.8 * sensorTemp.read_temperature()) + 32
       fahrenheitTens = int (math.trunc(fahrenheitRAW) / 10)
       fahrenheitOnes = math.trunc(fahrenheitRAW) % 10
       fahrenheitFractional = int ((fahrenheitRAW - math.trunc(fahrenheitRAW)) * 10)
       # Set temperature display fahrenheit
       segmentDisplay.set_digit(0, fahrenheitTens)          # Tens
       segmentDisplay.set_digit(1, fahrenheitOnes)          # Ones
       segmentDisplay.set_decimal(1, True)                  # Set decimal point
       segmentDisplay.set_digit(2, fahrenheitFractional)    # Tenths
       segmentDisplay.set_digit(3, 'F')                     # Fahrenheit unit
       print('Temp = {0:0.2f} *F'.format(fahrenheitRAW))
       segmentDisplay.write_display()       # write to the display
       displaywait()

while True:
   timedisplay()
   buttoncheck()
   tempdisplay(1)
   buttoncheck()
   tempdisplay(2)
   buttoncheck()
   
   
  
