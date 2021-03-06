import RPi.GPIO as GPIO
import time
import datetime
import pygame.mixer
from pygame.mixer import Sound
from yeelight import Bulb

### Button Definitions ###

# For Distance Sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# For Time Change / Alarm Toggle Buttons
GPIO_HOUR = 27
GPIO_MINUTE = 22
GPIO_HOLD_FOR_TIME = 23
GPIO_TOGGLE_ALARM = 10


### Init ###
# Alarm Sound Init
pygame.mixer.init()
sound = pygame.mixer.Sound("./Alarm.wav")

# LED Light Init
bulb = Bulb("192.168.43.2")
bulb = Bulb("192.168.43.2",auto_on = True, effect = "smooth", duration = 600000) # turns on in a duration of 10 minutes when light_on() is called

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
filer = open("./capstone-app/src/assets/alarm_time.txt","r")
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
  global alarm_enabled
  if (alarm_enabled):
    print("Disabling Alarm")
  else:
    print("Enabling Alarm")
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
    if (minute < 10):
      tempTime += "0" + str(minute)
    else:
      tempTime += str(minute)

    alarm_time = tempTime

    # Write alarm time to file
    filew = open("./capstone-app/src/assets/alarm_time.txt","w")
    filew.write(alarm_time)
    filew.close()
    time.sleep(0.5)

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
  print("Turning alarm on")

  # Make it do a procedural increase in volume eventually
  # To do this we can use sound.set_volume(x) 0 <= x <= 1
  sound.set_volume(0.1)
  sound.play()

def alarm_off(sound): 
  print("Turning alarm off")
  sound.stop()
    
def light_on(bulb):
  print("Turning light on")
  bulb.set_color_temp(4000) #sets the color temperature to match the sun
  bulb.turn_on()  #turns light on gradually within 10 minutes
    
def light_off(bulb):
  print("Turning light off")
  bulb.turn_off()

def turn_on_light_time(alarm):
  tempHr = ""
  tempMin = ""
  readHr = True
  for char in alarm:
    if (char == ':'):
      readHr = False
    elif (readHr):
      tempHr += char
    elif (not readHr):
      tempMin += char

  hour = int(tempHr)
  minute = int(tempMin)

  if (minute >= 10):
    minute -= 10
  else:
    if (hour == 0):
      hour = 24
    else:
      hour -= 1
    minute = 60 - (10 - minute)

  tempTime = str(hour) + ":"

  # Have to consider having a time like 8:1 when we want 8:01
  if (minute < 10):
    tempTime += "0" + str(minute)
  else:
    tempTime += str(minute)
  return tempTime

### When X time until alarm, start alarm processes ###
# If the alarm is disabled in this time we want this process to stop
# Need to test putting a sleep function in this, don't know if it will
# keep button functions from working...
is_light_on = False
while(True):
  # Going to overflow the I/O with this if the sleep doesnt work
  print("Running")
  if (alarm_enabled):
    #Update the sys time constantly
    sys_time = datetime.datetime.now().strftime('%H:%M')
    light_time = turn_on_light_time(alarm_time)
    # So with the light and alarm functions.. I'm not sure if
    # they will work on 1 thread of execution so we might have to
    # unfortunately multithread this :(
    print("Alarm Time: " + alarm_time)
    print("Light Time: " + light_time)
    print("Sys Time: " + sys_time)
    # As long as these if statements execute more than once per minute we are fine
    if ((light_time == sys_time) and (not is_light_on)):
      is_light_on = True 
      light_on(bulb)
 
    if (alarm_time == sys_time):
      alarm_on(sound)  #function that turns the alarm on
      # Add function to constantly check sensor distance
      delta = 5 # Need to figure this out more
      basket_made = False
      while (not basket_made):
        time.sleep(0.1)
        if (distance() < delta):
          basket_made = True
      # Add if distance is within threshold
      alarm_off(sound) #function that turns alarm off
      light_off(bulb) #function that turns light off
      is_light_on = False

  # Going to try and buffer everything with this sleep
  # might prevent buttons from working during the sleep but not sure
  time.sleep(0.5)
