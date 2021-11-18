#Functions for turning alarm on and off

import pygame.mixer

#not sure if I need these below:

from gpiozero import Sound
#from time import sleep
#from signal import pause

pygame.mixer.init()
sound = pygame.mixer.Sound("/home/pi/Music/Alarm.wav")

def alarm_on(sound):
		sound.play()    #sound should play at full volume by default
                        #use sound.set_volume() to set the volume of the speaker, set_volume(0.9) plays at 90% of full volume

def alarm_off(sound): 
		sound.stop()
