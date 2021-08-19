# A basic line following buggy, using all 3 sensors on the Line following board
# It assuems a dark line on a light background - such as on the move mat (www.kitronik.co.uk/46165)
#The line follow logic checks to see if the centre sensor is 'dark' and if so drives ahead,
#else it uses the difference between the side sensors to determine which way the buggy has turned and correct by reversing one of the motors.

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
import time

buggy = KitronikPicoRobotBuggy()

buggy.setLED(0,buggy.RED)
buggy.show()
time.sleep(1)
buggy.setLED(1,buggy.RED)
buggy.show()
time.sleep(1)
buggy.setLED(2,buggy.RED)
buggy.show()
time.sleep(1)
buggy.setLED(3,buggy.RED)
buggy.show()
time.sleep(1)
buggy.setLED(0,buggy.GREEN)
buggy.setLED(1,buggy.GREEN)
buggy.setLED(2,buggy.GREEN)
buggy.setLED(3,buggy.GREEN)
buggy.show()


while True:
    LeftVal = buggy.getRawLFValue("l")
    RightVal = buggy.getRawLFValue("r")
    CenterVal = buggy.getRawLFValue("c")
    #black line means centre should be high value, so if its not w eare off the line.
    if(CenterVal < 30000):
        #figure out which side we went
        if(LeftVal < (RightVal)):
            buggy.setLED(0,buggy.YELLOW)
            buggy.setLED(1,buggy.RED)
            buggy.setLED(2,buggy.RED)
            buggy.setLED(3,buggy.YELLOW)
            buggy.motorOn("l","f",75)
            buggy.motorOn("r","r",75)
        elif (RightVal <  (LeftVal)):
            buggy.setLED(0,buggy.RED)
            buggy.setLED(1,buggy.YELLOW)
            buggy.setLED(2,buggy.YELLOW)
            buggy.setLED(3,buggy.RED)
            buggy.motorOn("l","r",75)
            buggy.motorOn("r","f",75)
    else:
        buggy.setLED(0,buggy.GREEN)
        buggy.setLED(1,buggy.GREEN)
        buggy.setLED(2,buggy.GREEN)
        buggy.setLED(3,buggy.GREEN)
        buggy.motorOn("l","f",75)
        buggy.motorOn("r","f",75)
    buggy.show()
    time.sleep_ms(10)
    