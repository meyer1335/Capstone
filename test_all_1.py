import RPi.GPIO as GPIO
import time

# Init
# Lets us use pin numberings from board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup the buttons we want to use
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Read alarm_time.txt
filer = open("alarm_time.txt","r")
alarm_time = filer.read(10)
filer.close()

# Init alarm being enabled
# Later could make this based from config
alarm_enabled = True

# Init Distance Sensor and Buttons

# Button function for toggling the alarm
def toggle_alarm(channel):
  # Don't know if this line works B/C Python is weird af
  alarm_enabled = !alarm_enabled

# Button function for changing time
# This is writing back to the file going up to 
# 24 hours instead of 12 to keep track of AM/PM
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

    # If the other button to increment alarm time by hour is pressed
    # NOTE PIN NUMBER IS SUBJECT TO CHANGE
	  if (GPIO.input(18)):

	    print("Incrementing Alarm Time by 1 hour.")
	    
      # Do some string manipulation and change the alarm_time global var
      hour += 1
      if (hour == 24):
        hour = 0

    # If the other button to increment alarm time by minute is pressed
    # NOTE PIN NUMBER IS SUBJECT TO CHANGE
    elif (GPIO.input(19)):
      print("Incrementing Alarm Time by 1 minute.")

      # Do some string manipulation and change the alarm_time global var
      minute += 1
      if (minute == 60):
        minute = 0

    sleep(0.5)

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

  return

# Always be scanning for button presses

# This scans for if we should change the alarm time
GPIO.add_event_detect(17,GPIO.RISING,callback=change_alarm_time)

# This scans for if we should enable or disable the alarm
# The alarm is enabled by default (potentially add param for this later?)
GPIO.add_event_detect(20,GPIO.RISING,callback=toggle_alarm)


# When X time until alarm, start alarm processes
# If the alarm is disabled in this time we want this process to stop