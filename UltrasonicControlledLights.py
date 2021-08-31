# Showing the use of both ultrasonics to inidcate distance from front / rear 
#Green - long way to the nearest thing
#Yellow no more than 15cm to the nearest thing
#Red no more than 5cm to the nearest thing

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from utime import sleep_us

buggy = KitronikPicoRobotBuggy()
#start with the LEDs on green
buggy.setLED(0,buggy.GREEN)
buggy.setLED(1,buggy.GREEN)
buggy.setLED(2,buggy.GREEN)
buggy.setLED(3,buggy.GREEN)
buggy.show()

while True:
    frontDistance = buggy.getDistance("f")
    rearDistance = buggy.getDistance("r")
    #change LED colour depending on the distance measured
    if(frontDistance > 15):
        buggy.setLED(0,buggy.GREEN)
        buggy.setLED(1,buggy.GREEN)
    elif (frontDistance > 5):
        buggy.setLED(0,buggy.YELLOW)
        buggy.setLED(1,buggy.YELLOW)
    else:
        buggy.setLED(0,buggy.RED)
        buggy.setLED(1,buggy.RED)
    if(rearDistance>15):
        buggy.setLED(2,buggy.BLUE)
        buggy.setLED(3,buggy.BLUE)
    elif(rearDistance>5):
        buggy.setLED(2,buggy.YELLOW)
        buggy.setLED(3,buggy.YELLOW)
    else:
        buggy.setLED(2,buggy.RED)
        buggy.setLED(3,buggy.RED)
    buggy.show()
    sleep_us(50)
