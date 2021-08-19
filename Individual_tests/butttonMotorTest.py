#changes motors in sequence based on user buton pressing

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()
state = 0

def ButtonIRQHandler(pin):
    global state
    if pin == buggy.button:
        if state == 0:
            buggy.motorOn("l","f",100)
            buggy.motorOff("r")
            state = 1
        elif state == 1:
            buggy.motorOn("l","r",100)
            buggy.motorOff("r")
            state = 2
        elif state == 2:
            buggy.motorOn("r","f",100)
            buggy.motorOff("l")
            state = 3
        elif state ==3:
            buggy.motorOn("r","r",100)
            buggy.motorOff("l")
            state = 4
        elif state ==4:
            buggy.motorOn("l","f",100)
            buggy.motorOn("r","f",100)
            state = 5
        elif state ==5:
            buggy.motorOn("l","r",100)
            buggy.motorOn("r","r",100)
            state = 6
        else:
            buggy.motorOff("l")
            buggy.motorOff("r")
            state = 0

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   

while True:
    pass
