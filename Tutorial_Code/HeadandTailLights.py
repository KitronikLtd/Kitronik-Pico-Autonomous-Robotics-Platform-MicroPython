from PicoAutonomousRobotics import KitronikPicoRobotBuggy
buggy = KitronikPicoRobotBuggy()

buggy.setLED(0, buggy.WHITE)
buggy.setLED(1, buggy.WHITE)
buggy.setLED(2, buggy.RED)
buggy.setLED(3, buggy.RED)
buggy.show()
