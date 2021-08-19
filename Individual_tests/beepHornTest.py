#rotates ZIP LEDS to show 'alive', beeps horn whn button is pressed.

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()


def ButtonIRQHandler(pin):
    buggy.beepHorn()

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   

while True:
    buggy.setLED(3,buggy.BLUE)
    buggy.setLED(0,buggy.GREEN)
    buggy.setLED(1,buggy.YELLOW)
    buggy.setLED(2,buggy.RED)
    buggy.show()
    sleep(1)
    buggy.setLED(2,buggy.BLUE)
    buggy.setLED(3,buggy.GREEN)
    buggy.setLED(0,buggy.YELLOW)
    buggy.setLED(1,buggy.RED)
    buggy.show()
    sleep(1)
    buggy.setLED(1,buggy.BLUE)
    buggy.setLED(2,buggy.GREEN)
    buggy.setLED(3,buggy.YELLOW)
    buggy.setLED(0,buggy.RED)
    buggy.show()
    sleep(1)
    buggy.setLED(0,buggy.BLUE)
    buggy.setLED(1,buggy.GREEN)
    buggy.setLED(2,buggy.YELLOW)
    buggy.setLED(3,buggy.RED)
    buggy.show()
    sleep(1)
