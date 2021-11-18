import RPi.GPIO as GPIO
import time
import datetime
import pygame.mixer
from gpiozero import Sound
from yeelight import Bulb

### Button Definitions ###

# For Distance Sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# For Time Change / Alarm Toggle Buttons
GPIO_HOUR = 27
GPIO_MINUTE = 22
GPIO_HOLD_FOR_TIME = 23
GPIO_TOGGLE_ALARM = 25


### Init ###
# Alarm Sound Init
pygame.mixer.init()
sound = pygame.mixer.Sound("./Alarm.wav")

# LED Light Init
bulb = Bulb("192.168.43.2")

# Lets us use pin numberings from board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup the buttons we want to use
GPIO.setup(GPIO_HOUR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_MINUTE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_HOLD_FOR_TIME, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_TOGGLE_ALARM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup for distance sensor GPIO
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Read alarm_time.txt
filer = open("alarm_time.txt","r")
alarm_time = filer.read(10)
filer.close()

# Get time
sys_time = datetime.datetime.now().strftime('%H:%M')

# Init alarm being enabled
# Later could make this based from config
alarm_enabled = True

### Init Distance Sensor and Buttons ###

# Button function for toggling the alarm
def toggle_alarm(channel):
  # Don't know if this line works B/C Python is weird af
  alarm_enabled = not alarm_enabled

# Button function for changing time
# This is writing back to the file going up to 
# 24 hours instead of 12 to keep track of AM/PM
# Also the function to get time from Python works better like this
def change_alarm_time(channel):
  # Get the alarm time in the function
  global alarm_time
  
  # Read string val into local numbers to make manipulation easier
  tempHr = ""
  tempMin = ""
  readHr = True
  for char in alarm_time:
    if (char == ':'):
      readHr = False
    elif (readHr):
      tempHr += char
    elif (not readHr):
      tempMin += char

  hour = int(tempHr)
  minute = int(tempMin)

  # While the button that called this function is being held
  while(GPIO.input(channel)):

    # If the button to increment alarm time by hour is pressed
    if (GPIO.input(GPIO_HOUR)):

      print("Incrementing Alarm Time by 1 hour.")

      # Do some string manipulation and change the alarm_time global var
      hour += 1
      if (hour == 24):
        hour = 0

    # If the button to increment alarm time by minute is pressed
    elif (GPIO.input(GPIO_MINUTE)):
      print("Incrementing Alarm Time by 1 minute.")

      # Increment minute
      minute += 1
      if (minute == 60):
        minute = 0

    # Convert local alarm time back to global
    tempTime = str(hour) + ":"

    # Have to consider having a time like 8:1 when we want 8:01
    if (minute > 10):
      tempTime += "0" + minute
    else:
      tempTime += minute

    alarm_time = tempTime

    # Write alarm time to file
    filew = open("alarm_time.txt","w")
    filew.write(alarm_time)
    filew.close()
    sleep(0.5)

  return

### Always be scanning for button presses ##

# This scans for if we should change the alarm time
GPIO.add_event_detect(GPIO_HOLD_FOR_TIME,GPIO.RISING,callback=change_alarm_time)

# This scans for if we should enable or disable the alarm
# The alarm is enabled by default (potentially add param for this later?)
GPIO.add_event_detect(GPIO_TOGGLE_ALARM,GPIO.RISING,callback=toggle_alarm)

### Distance Sensor Code ###

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
	
def light_on(bulb):
	bulb.turn_on()
  # Make it do a procedural increase in brightness eventually
  # To do this we can use bulb.set_brightness(x) 0 <= x <= 100
	
def light_off(bulb):
	bulb.turn_off()

### When X time until alarm, start alarm processes ###
# If the alarm is disabled in this time we want this process to stop

