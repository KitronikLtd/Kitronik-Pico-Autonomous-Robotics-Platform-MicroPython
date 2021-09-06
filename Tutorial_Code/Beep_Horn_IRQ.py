from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()
def ButtonIRQHandler(pin):
    buggy.beepHorn()
    
buggy.button.irq(trigger=machine.Pin.IRQ_RISING, handler =  ButtonIRQHandler)  

while True:
   pass
  
