from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()
run = False

DegreesPerSecond = (6/5)*360

def ButtonIRQHandler(pin):
    global run
    if(run):
        run = False
    else:
        run = True

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   

def Forwards():
    buggy.motorOn("l","f",100)
    buggy.motorOn("r","f",100)
        
def Reverse():
    buggy.motorOn("l","r",100)
    buggy.motorOn("r","r",100)

def Stop():
    buggy.motorOff("r") 
    buggy.motorOff("l")

def Spin():
    buggy.motorOn("l","f",80)
    buggy.motorOn("r","r",80)

def TurnRight(HowFar):
    buggy.motorOn("l","f",80)
    buggy.motorOn("r","r",80)  
    sleep(HowFar/DegreesPerSecond)
    Stop()

def TurnLeft(HowFar):
    buggy.motorOn("l","r",80)
    buggy.motorOn("r","f",80)  
    sleep(HowFar/DegreesPerSecond)
    Stop()

def PenUp():
    buggy.goToPosition(2,45)

def PenDown():
    buggy.goToPosition(2,125)


while True:
   if(run):
        sleep(5) # wait so we can get the hand clear after pressing start.
        PenUp()
        Forwards()
        PenDown()
        for x in range (0,4):
            Forwards()
            sleep(0.5)
            TurnLeft(90)
        PenUp()
        run = False
    else:
        Stop()