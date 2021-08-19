#flicks servos form 0 to 180 and vice versa on button presses. Also changes ZIP LED colours at same time
from PicoAutonomousRobotics import KitronikPicoRobotBuggy

buggy = KitronikPicoRobotBuggy()
ServoAtZero = True

def ButtonIRQHandler(pin):
    global ServoAtZero
    if pin == buggy.button: 
        if ServoAtZero == True:
            ServoAtZero = False
        else:
            ServoAtZero = True


buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   
buggy.setLED(0,buggy.BLUE)
buggy.setLED(1,buggy.BLUE)
buggy.setLED(2,buggy.RED)
buggy.setLED(3,buggy.RED)
buggy.show()
buggy.goToPosition(0,0)
buggy.goToPosition(1,0)
buggy.goToPosition(2,0)
buggy.goToPosition(3,0)

while True:
    if(ServoAtZero):
        buggy.setLED(0,buggy.RED)
        buggy.setLED(1,buggy.RED)
        buggy.setLED(2,buggy.BLUE)
        buggy.setLED(3,buggy.BLUE)
        buggy.goToPosition(0,0)
        buggy.goToPosition(1,0)
        buggy.goToPosition(2,0)
        buggy.goToPosition(3,0)
        buggy.show()
    else:
        buggy.setLED(0,buggy.BLUE)
        buggy.setLED(1,buggy.BLUE)
        buggy.setLED(2,buggy.RED)
        buggy.setLED(3,buggy.RED)
        buggy.goToPosition(0,180)
        buggy.goToPosition(1,180)
        buggy.goToPosition(2,180)
        buggy.goToPosition(3,180)
        buggy.show()
