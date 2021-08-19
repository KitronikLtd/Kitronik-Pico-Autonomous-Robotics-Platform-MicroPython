#Step adds various bits of functionality so we can prove the current draws using the input button
from PicoAutonomousRobotics import KitronikPicoRobotBuggy

buggy = KitronikPicoRobotBuggy()
state = 0

def ButtonIRQHandler(pin):
    global state
    if pin == buggy.button:
        if state == 0:
            state = 1
        elif state == 1:
            state = 2
        elif state == 2:
            state = 3
        elif state == 3:
            state = 4
        else:
            state = 0

buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)   


while True:
    if state == 0: # Idle, nothing to do
        pass
    elif state == 1: # Buzzer and ultrasonics
        buggy.getDistance("f")
        buggy.getDistance("r")
        buggy.soundFrequency(350)
    elif state == 2: #adds full white ZIP LEDs
        buggy.soundFrequency(500)
        buggy.getDistance("f")
        buggy.getDistance("r")
        buggy.setLED(0,buggy.WHITE)
        buggy.setLED(1,buggy.WHITE)
        buggy.setLED(2,buggy.WHITE)
        buggy.setLED(3,buggy.WHITE)
        buggy.show()
    elif state ==3: #adds motors forward full power
        buggy.soundFrequency(1000)
        buggy.getDistance("f")
        buggy.getDistance("r")
        buggy.motorOn("l","f",100)
        buggy.motorOn("r","f",100)
        buggy.setLED(0,buggy.WHITE)
        buggy.setLED(1,buggy.WHITE)
        buggy.setLED(2,buggy.WHITE)
        buggy.setLED(3,buggy.WHITE)
        buggy.show()
    else: #turn off and shut up.
        buggy.setLED(0,buggy.BLACK)
        buggy.setLED(1,buggy.BLACK)
        buggy.setLED(2,buggy.BLACK)
        buggy.setLED(3,buggy.BLACK)
        buggy.show()
        buggy.silence()
        buggy.motorOff("l")
        buggy.motorOff("r")
    