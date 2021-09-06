from PicoAutonomousRobotics import KitronikPicoRobotBuggy

buggy = KitronikPicoRobotBuggy()
while True:
    distance = buggy.getDistance("f")
    if(distance < 1):
        red_channel = 0
        green_channel = 0
        blue_channel = 0
    elif(distance < 51): #0-50
        red_channel = 255
        green_channel = 5*distance
        blue_channel = 0
    elif(distance < 101): #51-100
        red_channel = 255-(5*(distance-51))
        green_channel = 255
        blue_channel = 0
    elif(distance < 150): #101 - 150
        red_channel = 0
        green_channel = 255
        blue_channel = (5*(distance-101))
    elif(distance < 201): #151-200
        red_channel = 0
        green_channel = 255-(5*(distance-151))
        blue_channel = 255
    else: #over 200
        red_channel = 0
        green_channel = 0
        blue_channel =255

    buggy.setLED(0,(int(red_channel),int(green_channel),int(blue_channel)))
    buggy.setLED(1,(int(red_channel),int(green_channel),int(blue_channel)))
    buggy.show()
