from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()
while True:
   frontDistance = buggy.getDistance("f")
   print("Front Distance:", frontDistance)
   sleep(1)
    
