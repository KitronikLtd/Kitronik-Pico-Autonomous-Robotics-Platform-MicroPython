#rotates colours on ZIP LEDs when the button is pressed

from PicoAutonomousRobotics import KitronikPicoRobotBuggy

buggy = KitronikPicoRobotBuggy()
LEDState = 0

def ButtonIRQHandler(pin):
    global LEDState
    global state
    if pin == buggy.button:
        if LEDState == 0:
            buggy.setLED(3,buggy.BLUE)
            buggy.setLED(0,buggy.GREEN)
            buggy.setLED(1,buggy.YELLOW)
            buggy.setLED(2,buggy.RED)
            LEDState = 1
        elif LEDState == 1:
            buggy.setLED(2,buggy.BLUE)
            buggy.setLED(3,buggy.GREEN)
            buggy.setLED(0,buggy.YELLOW)
            buggy.setLED(1,buggy.RED)
            LEDState = 2
        elif LEDState == 2:
            buggy.setLED(1,buggy.BLUE)
            buggy.setLED(2,buggy.GREEN)
            buggy.setLED(3,buggy.YELLOW)
            buggy.setLED(0,buggy.RED)
            LEDState = 3
        elif LEDState ==3:
            buggy.setLED(0,buggy.BLUE)
            buggy.setLED(1,buggy.GREEN)
            buggy.setLED(2,buggy.YELLOW)
            buggy.setLED(3,buggy.RED)
            LEDState = 4
        else:
            buggy.setLED(0,buggy.BLACK)
            buggy.setLED(1,buggy.BLACK)
            buggy.setLED(2,buggy.BLACK)
            buggy.setLED(3,buggy.BLACK)
            LEDState = 0
        buggy.show()

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   
buggy.setLED(0,buggy.WHITE)
buggy.setLED(1,buggy.WHITE)
buggy.setLED(2,buggy.WHITE)
buggy.setLED(3,buggy.WHITE)
buggy.show()

while True:
    pass