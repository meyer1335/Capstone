import RPi.GPIO as GPIO
import time

def button_callback(channel):
    global alarm_time
    print(alarm_time)
    while(GPIO.input(channel)):
	# This causes input delay. Might move
	# to inside the if statement
	time.sleep(0.5)
	if (GPIO.input(18)):
	    print(time.time())
	    print("Incrementing Alarm Time by 1 hour.")
	    #print(time.localtime())
	    alarm_time = "9:00"
    return alarm_time

str = ""
filer = open("alarm_time.txt","r")
alarm_time = filer.read(10)
print(alarm_time)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(17,GPIO.RISING,callback=button_callback)

while (not str == "x"):
    str = raw_input("Enter x to exit: ")

filer.close()
filew = open("alarm_time.txt","w")
filew.write(alarm_time)
filew.close()
GPIO.cleanup()

