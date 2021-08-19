# A  basic 'free roaming' robot
# uses the FRont and rear ultrasonic sensors to avoid obstacles
# if an ultrasonic is not fitted it will return -1
#uses the onboard button for a start / stop command via an IRQ.

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
import time

buggy = KitronikPicoRobotBuggy()
StartStop = False


def ButtonIRQHandler(pin):
    global StartStop
    if pin == buggy.button: 
        if StartStop == True:
            StartStop = False
        else:
            StartStop = True

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

buggy.setLED(0,buggy.PURPLE)
buggy.setLED(1,buggy.PURPLE)
buggy.setLED(2,buggy.PURPLE)
buggy.setLED(3,buggy.PURPLE)
buggy.show()

while True:
    if StartStop == True:
        frontdistance = buggy.getDistance("f")
        reardistance = buggy.getDistance("r")
        
        if(frontdistance > 15):
            #all clear, speed ahead
            buggy.setLED(0,buggy.GREEN)
            buggy.setLED(1,buggy.GREEN)
            buggy.setLED(2,buggy.GREEN)
            buggy.setLED(3,buggy.GREEN)
            buggy.motorOn("l","f",85)
            buggy.motorOn("r","f",85)
            
        elif (frontdistance > 5):
            #something in the way, but we (probably) have time to miss it
            buggy.setLED(0,buggy.GREEN)
            buggy.setLED(1,buggy.GREEN)
            buggy.setLED(2,buggy.GREEN)
            buggy.setLED(3,buggy.GREEN)
            buggy.motorOff("l")
            buggy.motorOff("r")
            if(reardistance>15):
                #there is space for us to reverse in a curve and try again
                buggy.setLED(0,buggy.BLUE)
                buggy.setLED(1,buggy.BLUE)
                buggy.setLED(2,buggy.BLUE)
                buggy.setLED(3,buggy.BLUE)
                buggy.motorOn("l","r",100)
                buggy.motorOn("r","r",50)
                time.sleep_ms(100)
            else:
                #spin on the spot 
                buggy.setLED(0,buggy.YELLOW)
                buggy.setLED(1,buggy.YELLOW)
                buggy.setLED(2,buggy.YELLOW)
                buggy.setLED(3,buggy.YELLOW)
                buggy.motorOn("l","f",100)
                buggy.motorOn("r","r",100)
        else:
            buggy.setLED(0,buggy.RED)
            buggy.setLED(1,buggy.RED)
            buggy.setLED(2,buggy.RED)
            buggy.setLED(3,buggy.RED)
            buggy.motorOn("l","r",100)
            buggy.motorOn("r","f",100)
        buggy.show()
    else:
        buggy.motorOff("l")
        buggy.motorOff("r")
        buggy.setLED(0,buggy.PURPLE)
        buggy.setLED(1,buggy.PURPLE)
        buggy.setLED(2,buggy.PURPLE)
        buggy.setLED(3,buggy.PURPLE)
        buggy.show()
    time.sleep_ms(50)
