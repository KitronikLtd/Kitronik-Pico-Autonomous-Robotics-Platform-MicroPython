from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep
buggy = KitronikPicoRobotBuggy()

brightness =10
countUp = True

def ButtonIRQHandler(pin):
    global countUp
    global brightness
    if(countUp):
        brightness +=5
        if(brightness>99):
            countUp = False
    else:
        brightness -=5
        if(brightness<1):
            countUp = True
    buggy.setBrightness(brightness)
    buggy.show()

def rotateColours():
    # temporarily  store the first one, then overwrite it, shifting by
    first = buggy.getLED(0)
    buggy.setLED(0,buggy.getLED(1))
    buggy.setLED(1,buggy.getLED(2))
    buggy.setLED(2,buggy.getLED(3))
    buggy.setLED(3,first) # push the colour that was at 0 back in at this end.

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)

#set the LEDs initial pattern
buggy.setLED(0, buggy.RED)
buggy.setLED(1, buggy.GREEN)
buggy.setLED(2, buggy.BLUE)
buggy.setLED(3, buggy.PURPLE)
buggy.setBrightness(brightness)
buggy.show()

while True:
    rotateColours()
    buggy.show()
    sleep(0.5)
