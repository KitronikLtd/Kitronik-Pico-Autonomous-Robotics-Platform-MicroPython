# Pico Autonomous Robotics Platform
# This is the micropython version of the module
# for Circuit python go to:
# https://github.com/KitronikLtd/Kitronik-Pico-Autonomous-Robotics-Platform-CircuitPython
# For more details on the product please visit
# https://www.kitronik.co.uk/5335

import array
from machine import Pin, PWM, ADC, time_pulse_us
from rp2 import PIO, StateMachine, asm_pio
from time import sleep, sleep_us, ticks_us

class KitronikPicoRobotBuggy:
    #button fo user input:
    button = Pin(0,Pin.IN,Pin.PULL_DOWN)
    
#Motors: controls the motor directions and speed for both motors
    def motorOn(self,motor, direction, speed):
        #cap speed to 0-100%
        if (speed<0):
            speed = 0
        elif (speed>100):
            speed=100
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
    #Servo 0 degrees -> pulse of 0.5ms, 180 degrees 2.5ms
    #pulse train freq 50hz - 20mS
    #1uS is freq of 1000000
    #servo pulses range from 500 to 2500usec and overall pulse train is 20000usec repeat.
    #servo pins on P.A.R.P. are: Servo 1: 21, Servo2 10, Servo 3 17, Servo 4 11
    maxServoPulse = 2500
    minServoPulse = 500
    pulseTrain = 20000
    degreesToUS = 2000/180
    
    #this code drives a pwm on the PIO. It is running at 2Mhz, which gives the PWM a 1uS resolution. 
    @asm_pio(sideset_init=PIO.OUT_LOW)
    def _servo_pwm():
    #first we clear the pin to zero, then load the registers. Y is always 20000 - 20uS, x is the pulse 'on' length.     
        pull(noblock) .side(0)
        mov(x, osr) # Keep most recent pull data stashed in X, for recycling by noblock
        mov(y, isr) # ISR must be preloaded with PWM count max
    #This is where the looping work is done. the overall loop rate is 1Mhz (clock is 2Mhz - we have 2 instructions to do)    
        label("loop")
        jmp(x_not_y, "skip") #if there is 'excess' Y number leave the pin alone and jump to the 'skip' label until we get to the X value
        nop()         .side(1)
        label("skip")
        jmp(y_dec, "loop") #count down y by 1 and jump to pwmloop. When y is 0 we will go back to the 'pull' command
             
    #doesnt actually register/unregister, just stops and starts the servo PIO
    def registerServo(self,servo):
        self.servos[servo].active(1)
    def deregisterServo(servo):
        self.servos[servo].active(0)
 
    # goToPosition takes a degree position for the serov to goto. 
    # 0degrees->180 degrees is 0->2000us, plus offset of 500uS
    #1 degree ~ 11uS.
    #This function does the sum then calls goToPeriod to actually poke the PIO 
    def goToPosition(self,servo, degrees):
        pulseLength = int(degrees*self.degreesToUS + 500)
        self.goToPeriod(servo,pulseLength)
    
    def goToPeriod(self,servo, period):
        if(period < 500):
            period = 500
        if(period >2500):
            period =2500
        self.servos[servo].put(period)
        
    def _initServos(self):
        servoPins = [21,10,17,11]
        for i in range(4):
            self.servos.append (StateMachine(i, self._servo_pwm, freq=2000000, sideset_base=Pin(servoPins[i])))
            self.servos[i].put(self.pulseTrain)
            self.servos[i].exec("pull()")
            self.servos[i].exec("mov(isr, osr)")
            
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
        setLED(whichLED,self.BLACK)
        
    #sets the colour of an individual LED. Use show to make change visible
    def setLED(self,whichLED, whichColour):
        if(whichLED<0):
            raise Exception("INVALID LED:",whichLED," specified")
        elif(whichLED>3):
            raise Exception("INVALID LED:",whichLED," specified")
        else:
            self.theLEDs[whichLED] = (whichColour[1]<<16) + (whichColour[0]<<8) + whichColour[2]
    
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
        if(timepassed ==-1): #timeout - range equivalent of 5 meters - past the sensors limit or not fitted
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
    
    def setLFDarkValue(self,darkThreshold):
        self.darkVal = darkThreshold
        
    def setLFLightValue(self,lightThreshold):
        self.lightVal = lightThreshold
        
    #this returns True when sensor is over light and FALSE over Dark.
    #Light/Dark is determined by the thresholds.
    def isLFSensorLight(self,whichSensor):
        if(whichSensor == "c"):
            sensorVal = self.CentreLF.read_u16()
        elif (whichSensor == "l"):
            sensorVal = self.LeftLF.read_u16()
        elif (whichSensor == "r"):
            sensorVal = self.RightLF.read_u16()
        else:
            raise Exception("INVALID SENSOR") #harsh, but at least you'll know
        if(sensorVal>self.darkVal):
            return False
        elif(sensorVal<self.lightVal):
            return True
        else:
            raise Exception("Sensor value 'Grey'")

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
        self.motor1Forward=PWM(Pin(20))
        self.motor1Reverse=PWM(Pin(19))
        self.motor2Forward=PWM(Pin(6))
        self.motor2Reverse=PWM(Pin(7))
        #set the PWM to 10Khz
        self.motor1Forward.freq(10000)
        self.motor1Reverse.freq(10000)
        self.motor2Forward.freq(10000)
        self.motor2Reverse.freq(10000)
        self.servos = []
        self._initServos()
        #connect the servos by default on construction - advanced uses can disconnect them if required.
        for i in range(4):
            self.registerServo(i)
            self.goToPosition(i,90) #set the servo outputs to middle of the range.
        # Create  and start the StateMachine for the ZIPLeds
        self.ZIPLEDs = StateMachine(4, self._ZIPLEDOutput, freq=8_000_000, sideset_base=Pin(18))
        self.theLEDs = array.array("I", [0 for _ in range(4)]) #an array for the LED colours.
        self.brightness = 0.2 #20% initially 
        self.ZIPLEDs.active(1)
        #set the measurements to metric by default.
        self.conversionFactor = 0.0343
        self.maxDistanceTimeout = int( 2 * 500 /self.conversionFactor) # 500cm is past the 400cm max range by a reasonable amount for a timeout
        self.buzzer = PWM(Pin(16))
        #setup LineFollow Pins
        self.CentreLF = ADC(27)
        self.LeftLF = ADC(28)
        self.RightLF = ADC(26)
        #The LF circuit is setup to give a high value when a dark (non reflective) surface is in view,and a low value when a light (reflective) surface is in view.
        #To aid there is a 'is it light or dark' function, and these values set the thresholds for determining that.
        self.LightVal = 30000 
        self.DarkVal = 35000
    
