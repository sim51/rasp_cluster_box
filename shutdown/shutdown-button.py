#!/usr/bin/python

# When button is pressed, we shutdown the server and blink the little red led (#17)

import RPi.GPIO as GPIO
import os
import time
import subprocess

# Set GPIO mode that match the board number
GPIO.setmode(GPIO.BCM)

# Setup to on the little red led
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)

# GPIO for button with a pull down resistance (for pull_up : GPIO_PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# We wait until the button is pushed
GPIO.wait_for_edge(4, GPIO.RISING)

# Execute a shutdown order
command = "/usr/bin/sudo /sbin/shutdown -h now"
subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Blink the little red led
try:
  while True:
    GPIO.output(17,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.1)
    
except KeyboardInterrupt:
  GPIO.cleanup()

GPIO.cleanup()  
exit(0)
