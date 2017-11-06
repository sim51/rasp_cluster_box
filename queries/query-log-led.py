#!/usr/bin/python

# when a new query appears into log file, blink the little green led (#25)

import RPi.GPIO as GPIO
import os
import time
import tail

# Some varaibles
logFile = "/opt/neo4j/logs/query.log"
blinkTime = 0.1

# Set GPIO mode that match the board number
GPIO.setmode(GPIO.BCM)

# Setup to on the little red led
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)

# What we do when a new query appers ?
try:
  for data in tail.follow(logFile):
    GPIO.output(25, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(25,GPIO.LOW)
    
except KeyboardInterrupt:
  GPIO.cleanup()

exit(0)
