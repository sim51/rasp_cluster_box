#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os

# Set GPIO mode that match the board number
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)

# Blink the little red led
try:
  while True:
    time.sleep(0.1)
    
except KeyboardInterrupt:
  GPIO.cleanup()

exit(0)
