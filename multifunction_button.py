#!/usr/bin/python3
from gpiozero import Button
from signal import pause
import os

# connect your button to appropiate pin + ground
# pi 3: gpio 21 is pin 40, gpio 7 is pin 26, gpio 3 is pin 5
# (only gpio 3 - pin 5 has power ON functionality)
offGPIO = 3
holdTime = 5
numPushed = 0


# pi3: led0 green, led1 red
def shutdown():
    global numPushed
    if numPushed > 6:
        os.system("echo heartbeat | sudo tee /sys/class/leds/led1/trigger")
        os.system("echo timer | sudo tee /sys/class/leds/led0/trigger")
    if numPushed == 6:
        os.system("echo $(date) Powering Off")
        os.system("echo none | sudo tee /sys/class/leds/led0/trigger")
        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness")
        os.system("echo timer | sudo tee /sys/class/leds/led1/trigger")
        os.system("sudo poweroff")
    if numPushed == 4:
        os.system("echo $(date) Docker Service Stopped")
        os.system("echo none | sudo tee /sys/class/leds/led1/trigger")
        os.system("echo 1 | sudo tee /sys/class/leds/led1/brightness")
        os.system("docker compose -f /home/pi/service/docker-compose.yml stop")
    if numPushed == 2:
        os.system("echo $(date) Docker Service Pause")
        os.system("echo none | sudo tee /sys/class/leds/led0/trigger")
        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness")
        os.system("docker compose -f /home/pi/service/docker-compose.yml pause")
    os.system("echo resetting numPushed({}) to 0".format(numPushed))
    numPushed = 0


def when_pressed():
    global numPushed
    numPushed += 1
    # start green heartbeat, red timer while pressed
    os.system("echo $(date) button pressed {} times".format(numPushed))
    os.system("echo timer | sudo tee /sys/class/leds/led1/trigger")
    os.system("echo heartbeat | sudo tee /sys/class/leds/led0/trigger")


def when_released():
    # be sure to turn back to green timer, red heartbeat if released
    os.system("echo $(date) button released")
    os.system("echo heartbeat | sudo tee /sys/class/leds/led1/trigger")
    os.system("echo timer | sudo tee /sys/class/leds/led0/trigger")


btn = Button(offGPIO, hold_time=holdTime)
btn.when_held = shutdown
btn.when_pressed = when_pressed
btn.when_released = when_released
pause()  # handle the button presses in the background
