# Pico Autonomous Robotics Platform
# This is the micropython version of the module
# Version 1.0 Initial Release
# For more details on the product please visit
# https://www.kitronik.co.uk/5335

import array
from machine import Pin, PWM, ADC, time_pulse_us
from rp2 import PIO, StateMachine, asm_pio
from time import sleep, sleep_ms, sleep_us, ticks_us

# List of which StateMachines we have used
usedSM = [False, False, False, False, False, False, False, False]

class KitronikPicoRobotBuggy:
    #button fo user input:
    button = Pin(0,Pin.IN,Pin.PULL_DOWN)
    
#Motors: controls the motor directions and speed for both motors
    def _initMotors(self):
        self.motor1Forward=PWM(Pin(20))
        self.motor1Reverse=PWM(Pin(19))
        self.motor2Forward=PWM(Pin(6))
        self.motor2Reverse=PWM(Pin(7))
        #set the PWM to 100Hz
        self.motor1Forward.freq(100)
        self.motor1Reverse.freq(100)
        self.motor2Forward.freq(100)
        self.motor2Reverse.freq(100)
        self.motorOff("l")
        self.motorOff("r")
        
    def motorOn(self,motor, direction, speed, jumpStart=False):
        #cap speed to 0-100%
        if (speed<0):
            speed = 0
        elif (speed>100):
            speed=100
        
        frequency = 100
        if (speed < 15):
            frequency = 20
        elif (speed < 20):
            frequency = 50
            
        
        self.motor1Forward.freq(frequency)
        self.motor1Reverse.freq(frequency)
        self.motor2Forward.freq(frequency)
        self.motor2Reverse.freq(frequency)
        
        # Jump start motor by setting to 100% for 20 ms,
        # then dropping to speed specified.
        # Down to jump start the motor when set at low speed
        if (not jumpStart and speed > 0.1 and speed < 35):
            self.motorOn(motor, direction, 100, True)
            sleep_ms(20)

        #convert 0-100 to 0-65535
        PWMVal = int(speed*655.35)
        if motor == "l":
            if direction == "f":
                self.motor1Forward.duty_u16(PWMVal)
                self.motor1Reverse.duty_u16(0)
            elif direction == "r":
                self.motor1Forward.duty_u16(0)
                self.motor1Reverse.duty_u16(PWMVal)
            else:
                raise Exception("INVALID DIRECTION") #harsh, but at least you'll know
        elif motor == "r":
            if direction == "f":
                self.motor2Forward.duty_u16(PWMVal)
                self.motor2Reverse.duty_u16(0)
            elif direction == "r":
                self.motor2Forward.duty_u16(0)
                self.motor2Reverse.duty_u16(PWMVal)
            else:
                raise Exception("INVALID DIRECTION") #harsh, but at least you'll know
        else:
            raise Exception("INVALID MOTOR") #harsh, but at least you'll know
    #To turn off set the speed to 0...
    def motorOff(self,motor):
        self.motorOn(motor,"f",0)
        
#ServoControl:
    #doesnt actually register/unregister, just stops and starts the servo PIO
    def registerServo(self, servo):
        self.servos[servo] = PWM(Pin(self.servoPins[servo]))
        self.servos[servo].freq(50)
        self.goToPosition(servo, 90)

    def deregisterServo(self, servo):
        self.servos[servo].deinit()
 
    def scale(self, value, fromMin, fromMax, toMin, toMax):
        return toMin + ((value - fromMin) * ((toMax - toMin) / (fromMax - fromMin)))
 
    # goToPosition takes a degree position for the serov to goto. 
    # 0degrees->180 degrees is 0->2000us, plus offset of 500uS
    #1 degree ~ 11uS.
    #This function does the sum then calls goToPeriod to actually poke the PIO 
    def goToPosition(self,servo, degrees):
        if degrees < 0:
            degrees = 0
        if degrees > 180:
            degrees = 180
        scaledValue = self.scale(degrees, 0, 180, 1638, 8192)
        self.servos[servo].duty_u16(int(scaledValue))
    
    def goToPeriod(self,servo, period):
        if period < 500:
            period = 500
        if period > 2500:
            period = 2500
        scaledValue = self.scale(period, 500, 2500, 1638, 8192)
        self.servos[servo].duty_u16(int(scaledValue))
        
    def _initServos(self):
        self.servoPins = [21,10,17,11]
        self.servos = [None for _ in range(4)]
        #connect the servos by default on construction - advanced uses can disconnect them if required.
        for i in range(4):
            self.registerServo(i)
            
#ZIPLEDS
#We drive the ZIP LEDs using one of the PIO statemachines. 
    @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
    def _ZIPLEDOutput():
        T1 = 2
        T2 = 5
        T3 = 3
        wrap_target()
        label("bitloop")
        out(x, 1)               .side(0)    [T3 - 1]
        jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
        jmp("bitloop")          .side(1)    [T2 - 1]
        label("do_zero")
        nop()                   .side(0)    [T2 - 1]
        wrap()
        
    #define some colour tuples for people to use.    
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (255, 255, 255)
    COLOURS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)
    
    #sow pushes the current setup of theLEDS to the physical LEDS - it makes them visible.
    def show(self):
        brightAdjustedLEDs = array.array("I", [0 for _ in range(4)])
        for i,c in enumerate(self.theLEDs):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            brightAdjustedLEDs[i] = (g<<16) + (r<<8) + b
        self.ZIPLEDs.put(brightAdjustedLEDs, 8)
    def clear(self,whichLED):
        self.setLED(whichLED,self.BLACK)
        
    #sets the colour of an individual LED. Use show to make change visible
    def setLED(self,whichLED, whichColour):
        if(whichLED<0):
            raise Exception("INVALID LED:",whichLED," specified")
        elif(whichLED>3):
            raise Exception("INVALID LED:",whichLED," specified")
        else:
            self.theLEDs[whichLED] = (whichColour[1]<<16) + (whichColour[0]<<8) + whichColour[2]
    
    #gets the stored colour of an individual LED, which isnt nessecerily the colour on show if it has been changed, but not 'show'n
    def getLED(self,whichLED):
        if(whichLED<0):
            raise Exception("INVALID LED:",whichLED," specified")
        elif(whichLED>3):
            raise Exception("INVALID LED:",whichLED," specified")
        else:
            return(((self.theLEDs[whichLED]>>8) & 0xff), ((self.theLEDs[whichLED]>>16)& 0xff) ,((self.theLEDs[whichLED])& 0xff))
    
    #takes 0-100 as a brightness value, brighness is applies in the'show' function
    def setBrightness(self, value):
            #cap to 0-100%
        if (value<0):
            value = 0
        elif (value>100):
            value=100
        self.brightness = value / 100

#Ultrasonic:
    #there are 2 Ultrasonic headers. The front one is the default if not explicitly called wth 'r' for rear
    # if we get a timeout (which would be a not fitted sensor, or a range over the sensors maximium the distance returned is -1           
    def getDistance(self, whichSensor = "f"):
        trigger = Pin(14, Pin.OUT)
        echo = Pin(15, Pin.IN)
        if(whichSensor == "r"):
            trigger = Pin(3, Pin.OUT) #rear
            echo = Pin(2, Pin.IN)
        trigger.low()
        sleep_us(2)
        trigger.high()
        sleep_us(5)
        trigger.low()
        timePassed = time_pulse_us(echo, 1, self.maxDistanceTimeout)
        if(timePassed ==-1): #timeout - range equivalent of 5 meters - past the sensors limit or not fitted
            distance = -1
        else:
            distance = (timePassed * self.conversionFactor) / 2
        return distance
       
    def setMeasurementsTo(self,units):
        #0.0343 cm per microsecond or 0.0135 inches
        if(units == "inch"):
            self.conversionFactor = 0.0135 #if you ask nicely we can do imperial
        else:
            self.conversionFactor = 0.0343 #cm is default - we are in  metric world.

#Linefollower: there are 3 LF sensors on the plug in board.        
    #gets the raw (0-65535) value of the sensor. 65535 is full dark, 0 would be full brightness.
    #in practice the values tend to vary between approx 5000 - 60000   
    def getRawLFValue(self,whichSensor):
        if(whichSensor == "c"):
            return self.CentreLF.read_u16()
        elif (whichSensor == "l"):
            return self.LeftLF.read_u16()
        elif (whichSensor == "r"):
            return self.RightLF.read_u16()
        else:
            raise Exception("INVALID SENSOR") #harsh, but at least you'll know
            return 0 #just in case
    
    #These functions set the thresholds for light/dark sensing to return true / false
    #there should be a gap between light and dark thresholds, to give soem deadbanding.
    #if specified OptionalLeftThreshold and OptionalRightThreshold give you the ability to
    #specify 3 sets of values. If missing then all sensors use the same value.
    #initially all sensors are set to 30000  for light and 35000 for dark.
        
    def setLFDarkValue(self,darkThreshold, OptionalLeftThreshold = -1, OptionalRightThreshold = -1):
        self.centreDarkVal = darkThreshold
        if(OptionalLeftThreshold == -1):
            self.leftDarkVal = darkThreshold
        else:
            self.leftDarkVal = OptionalLeftThreshold
        if(OptionalRightThreshold == -1):
            self.rightDarkVal = darkThreshold
        else:
            self.rightDarkVal = OptionalRightThreshold
        
    def setLFLightValue(self,lightThreshold, OptionalLeftThreshold = -1, OptionalRightThreshold = -1):
        self.centreLightVal = lightThreshold
        if(OptionalLeftThreshold == -1):
            self.leftLightVal = lightThreshold
        else:
            self.leftLightVal = OptionalLeftThreshold
        if(OptionalRightThreshold == -1):
            self.rightLightVal = lightThreshold
        else:
            self.rightLightVal = OptionalRightThreshold
 
    #this returns True when sensor is over light and FALSE over Dark.
    #Light/Dark is determined by the thresholds.
    # This code will throw an exception if the value returned is in the 'gery' area.
    #This can happen is you sample half on /off a line for instance.
    #Setting the thresholds to the same value will negate this functionality
    def isLFSensorLight(self,whichSensor):
        if(whichSensor == "c"):
            sensorVal = self.CentreLF.read_u16()
            if(sensorVal >= self.centreDarkVal):
                return False
            elif(sensorVal < self.centreLightVal):
                return True
            else:
                raise Exception("Sensor value 'Grey'")
        elif (whichSensor == "l"):
            sensorVal = self.LeftLF.read_u16()
            if(sensorVal >= self.leftDarkVal):
                return False
            elif(sensorVal < self.leftLightVal):
                return True
            else:
                raise Exception("Sensor value 'Grey'")            
        elif (whichSensor == "r"):
            sensorVal = self.RightLF.read_u16()
            if(sensorVal >= self.rightDarkVal):
                return False
            elif(sensorVal < self.rightLightVal):
                return True
            else:
                raise Exception("Sensor value 'Grey'")
        else:
            raise Exception("INVALID SENSOR") #harsh, but at least you'll know

#Buzzer: functions will sound a horn or a required frequency. Option aswell to silence the buzzer
    def silence(self):
        self.buzzer.duty_u16(0) #silence by setting duty to 0
        
    def soundFrequency(self,frequency):
        if (frequency<0):
            frequency = 0
        elif (frequency>3000):
            frequency=3000
        self.buzzer.freq(frequency) #1khz. Find out the limits of PWM on the Pico - doesn seem to make a noise past 3080hz
        self.buzzer.duty_u16(32767) #50% duty
        
    def beepHorn(self):
        self.soundFrequency(350)
        sleep(0.3)
        self.silence()

#initialisation code for using:
    #defaults to the standard pins and freq for the kitronik board, but could be overridden
    def __init__(self):
        self._initMotors()
        self.servos = []
        self._initServos()
        #connect the servos by default on construction - advanced uses can disconnect them if required.
        for i in range(4):
            self.registerServo(i)
            self.goToPosition(i,90) #set the servo outputs to middle of the range.
        # Create  and start the StateMachine for the ZIPLeds
        for i in range(8): # StateMachine range from 0 to 7
            if usedSM[i]:
                continue # Ignore this index if already used
            try:
                self.ZIPLEDs = StateMachine(i, self._ZIPLEDOutput, freq=8_000_000, sideset_base=Pin(18))
                usedSM[i] = True # Set this index to used
                break # Have claimed the SM, can leave now
            except ValueError:
                pass # External resouce has SM, move on
            if i == 7:
                # Cannot find an unused SM
                raise ValueError("Could not claim a StateMachine, all in use")
        
        self.theLEDs = array.array("I", [0 for _ in range(4)]) #an array for the LED colours.
        self.brightness = 0.2 #20% initially 
        self.ZIPLEDs.active(1)
        #set the measurements to metric by default.
        self.conversionFactor = 0.0343
        self.maxDistanceTimeout = int( 2 * 500 /self.conversionFactor) # 500cm is past the 400cm max range by a reasonable amount for a timeout
        self.buzzer = PWM(Pin(16))
        self.buzzer.duty_u16(0) #ensure silence by setting duty to 0
        #setup LineFollow Pins
        self.CentreLF = ADC(27)
        self.LeftLF = ADC(28)
        self.RightLF = ADC(26)
        #The LF circuit is setup to give a high value when a dark (non reflective) surface is in view,and a low value when a light (reflective) surface is in view.
        #To aid there is a 'is it light or dark' function, and these values set the thresholds for determining that.
        self.centreLightVal = 30000 
        self.centreDarkVal = 35000
        self.leftLightVal = 30000 
        self.leftDarkVal = 35000
        self.rightLightVal = 30000 
        self.rightDarkVal = 35000
    
