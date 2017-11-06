#!/usr/bin/python

# Look at neo4j endpoint to know the status of the node
# leader => big yellow blink (#22)
# follower => big yellow (#22)
# replica => big greeen (#24)
# Server is starter => big red (#27)

import RPi.GPIO as GPIO
import os
import time
import requests

# Some varaibles
leaderUrl = "http://localhost:7474/db/manage/server/core/writable"
followerUrl = "http://localhost:7474/db/manage/server/core/read-only"
replicaUrl = "http://localhost:7474/db/manage/server/read-replica/available"
avaibleUrl = "http://localhost:7474/"
repeatTime = 1

# Set GPIO mode that match the board number
GPIO.setmode(GPIO.BCM)

# Setup to off all led
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)



try:
  
  while True:
  
    try:
    
      r = requests.get(avaibleUrl)
      if r.status_code == 200:
        
        # Server is up
        GPIO.output(27, GPIO.HIGH)
        
        r2 = requests.get(leaderUrl)
        if r2.status_code == 200:
          # leader blink 24
          GPIO.output(22, not GPIO.input(22))
          GPIO.output(24, GPIO.LOW)
        
        r3 = requests.get(followerUrl)
        if r3.status_code == 200:
          # follower full 24
          GPIO.output(22, GPIO.HIGH)
          GPIO.output(24, GPIO.LOW)
        
        r4 = requests.get(replicaUrl)
        if r4.status_code == 200:
          # replica full 22
          GPIO.output(24, GPIO.HIGH)
          GPIO.output(22, GPIO.LOW)
      
      else:
          GPIO.output(27, not GPIO.input(22))
          GPIO.output(24, not GPIO.input(22))
          GPIO.output(22, not GPIO.input(22))
      
      
      time.sleep(repeatTime)
      
    except requests.ConnectionError:
      GPIO.output(27, not GPIO.input(22))
      GPIO.output(24, not GPIO.input(22))
      GPIO.output(22, not GPIO.input(22))
    
except KeyboardInterrupt:
  GPIO.cleanup()

exit(0)
