# Kitronik-Pico-Autonomous-Robotics-Platform-MicroPython
A class and sample code for the Kitronik Autonomous Robotics Platform for the Raspberry Pi Pico. (www.kitronik.co.uk/5335)

This is the MicroPython version. For Circuit Python see: 
https://github.com/KitronikLtd/Kitronik-Pico-Autonomous-Robotics-Platform-CircuitPython

To use save PicoAutonomusRobotics.py file onto the Pico so it can be imported
## Import PicoAutonomusRobotics.py and construct an instance:
    import PicoAutonomusRobotics
    robot = PicoAutonomusRobotics.KitronikPicoRobotBuggy()

This will setup the correct pins to drive the motors. 
## Drive a motor:
    robot.motorOn(motor, direction, speed)
where:
* motor => 1 or 2
* direction => f or r
* speed => 0 to 100
## Stop a motor:
    robot.motorOff(motor)
where:
* motor => 1 or 2

## Read Ultrasonic Distance:



### To turn on ZIP LEDs:



Look at the function headers and function comments for more detail if you need to change them.

# Troubleshooting

This code is designed to be used as a module. See: https://kitronik.co.uk/blogs/resources/modules-micro-python-and-the-raspberry-pi-pico for more information
