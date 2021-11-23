import RPi.GPIO as GPIO
import pygame.mixer
from pygame.mixer import Sound

# For Distance Sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# Alarm Sound Init
pygame.mixer.init()
sound = pygame.mixer.Sound("./Alarm.wav")

# Lets us use pin numberings from board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup for distance sensor GPIO
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Init alarm being enabled
alarm_enabled = True

def distance():
  # set Trigger to HIGH
  GPIO.output(GPIO_TRIGGER, True)
 
  # set Trigger after 0.01ms to LOW
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
 
  StartTime = time.time()
  StopTime = time.time()
 
  # save StartTime
  while GPIO.input(GPIO_ECHO) == 0:
    StartTime = time.time()
 
  # save time of arrival
  while GPIO.input(GPIO_ECHO) == 1:
    StopTime = time.time()
 
  # time difference between start and arrival
  TimeElapsed = StopTime - StartTime
  # multiply with the sonic speed (34300 cm/s)
  # and divide by 2, because there and back
  distance = (TimeElapsed * 34300) / 2
 
  return distance

def alarm_on(sound):
  # Make it do a procedural increase in volume eventually
  # To do this we can use sound.set_volume(x) 0 <= x <= 1
  sound.play()

def alarm_off(sound): 
  sound.stop()

while(True):
  print("Running")

  # Turn on alarm
  alarm_on(sound)

  # If distance < THRESHOLD turn off alarm
  if (distance < 1):
    alarm_off(sound)

  sleep(0.5)