# Kitronik-Pico-Autonomous-Robotics-Platform-MicroPython
A class and sample code for the Kitronik Autonomous Robotics Platform for the Raspberry Pi Pico. (www.kitronik.co.uk/5335)

This is the MicroPython version. For Circuit Python see: 
https://github.com/KitronikLtd/Kitronik-Pico-Autonomous-Robotics-Platform-CircuitPython

On the Autonomous Robotics Platform :  
    Forward is defined as the end away from the power switch / castor.  
    Left and Right are defined when facing Forward  
    The Pico should be inserted with the USB connector facing the rear (away from the Pen hole)  
  
To use save PicoAutonomusRobotics.py file onto the Pico so it can be imported.
## Import PicoAutonomusRobotics.py and construct an instance:
```python
    import PicoAutonomusRobotics
    robot = PicoAutonomusRobotics.KitronikPicoRobotBuggy()
 ```
This will setup the various correct pins for motors / servos / sensors.

## Drive a motor:
```python
    robot.motorOn(motor, direction, speed)
```
where:
* motor => "l" or "r" (left or right)
* direction => "f" or "r" (forward or reverse)
* speed => 0 to 100
## Stop a motor:
```python
    robot.motorOff(motor)
```
where:
* motor => 1 or 2

## Servos
The servo PWM (20mS repeat, on period capped between 500 and 2500uS) is driven using the Pico PIO.  
The servos are registered automatically in the initalisation of the class.   
This process sets the PIO PWM active on the servo pin.  
If the pin is needed for another purpose it can be 'deregistered' which sets te PIO to inactive.  
 ```python
    robot.deregisterServo(servo)
 ```
To re-register a servo after it has been de-registered:  
```python
    robot.registerServo(servo)
```
where:
* servo => the servo number (0-3)


### Drive a servo 

```python 
    robot.goToPosition(servo, degrees):
```
where:
* servo => 0-3 for the servo to control
* degrees => 0-180


```python 
    robot.goToPeriod(servo, period)
 ```   
where:
* servo => 0-3 for the serov to control
* period => 500-2500 in uS


## Read Ultrasonic Distance:
```python 
robot.getDistance(whichSensor):
```
where 
* whichSensor => "f" or "r" for front or rear sensor.
This parameter is defaulted to "f" so the call can be 
```python
robot.getDistance()
```

Setup the units  
```python
robot.setMeasurementsTo(units):
```
where:
* units => "inch" for imperial (inch) measurements, "cm" for metric (cm) measuerments

## Line Following
Sensors are marked on the sensor PCB for left, right, and centre. Left is defined as on the left side when looking down on the buggy, facing the front.  
The centre sensor is slightly ahead of the side sensors.
```python
robot.getRawLFValue(WhichSensor):
```
returns:
* the raw sensor value - 0-65535. Low numbers represent dark surfaces.  

where:
* whichSensor => "c", "l", "r" (central, left or right sensor)

The line following can also return true or false:
```python
robot.isLFSensorLight(whichSensor):
```
returns:  
* True when sensor is over a light surface and False when over a dark surface.

The light / dark determination is based on the values in darkThreshold and lightThreshold  

where: 
* whichSensor => "l","r", or "c"

To set the thresholds use:
```python
robot.setLFDarkValue(darkThreshold):
```
```python
robot.setLFLightValue(lightThreshold):
```
Typical values for 'Light' surfaces would be under 20000, and for 'Dark' surfaces over 30000.
    
## Buzzer
The buzzer is driven with a PWM pin.  
To sound the buzzer:  
        
```python
robot.soundFrequency(frequency)
```
where:
  * frequency => 0-3000 - the frequency to sound

```python
robot.silence()
```
silences the buzzer

```python        
robot.beepHorn():
```
beeps the buzzer like a car horn.

## To turn on ZIP LEDs:
ZIP LEDs have a 2 stage operation.  
To set the LEDs with the colour required:  
```python
robot.setLED(whichLED, whichColour)
```
where:  
    * whichLED => 0-3  
    * whichColour => tuple of ( Red Value, Green Value, Blue Value), or one of the pre defined colours:
    
```python
COLOURS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)
```
To turn off the LEDs call 
```python
robot.clear(whichLED)
```
where:  
    * whichLED => 0-3

To control the brightness
```python
robot.setBrightness(value):
```
where:  
* value => brightness value 0-100

then to make the changes visible call:

```python
robot.show():
```

# Troubleshooting

This code is designed to be used as a module. See: https://kitronik.co.uk/blogs/resources/modules-micro-python-and-the-raspberry-pi-pico for more information


