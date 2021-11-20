import time
import warnings
import json 
from modelobject import * 
RANGE = 100 


def _clamp(value, min, max):
    if value is None:
        return None
    elif (value > max):
        return max
    elif (value < min):
        return min
    return value

class PID_settings(object): 
    def __init__(self, name): 
        self.name = name
        self.Kp, self.Ki, self.Kd = 3.0 , 0 , 0
        self.setpoint = 0
        self.sample_time = 0
        self._min_output = 0
        self._max_output = 100
        self._auto_mode = True
        
        #self.error_map = None


    def setLoopModeAuto(self,_auto_mode):
        if(type(_auto_mode) == bool): 
            self._auto_mode = _auto_mode
        else:
            return 
 
 

    def writefile(self): 
        with open('data.txt', 'w') as outfile:
            json.dump(self.__dict__, outfile)
        jsonStr = json.dumps(self.__dict__)
        print(jsonStr)
        # return jsonStr

    def readfile(self): 
        with open('data.txt') as infile:
            self.__dict__ = json.load(infile)
    

    
    def setgain(self,Kp,Ki,Kd): 
        if(Kp>=0 and Kp<RANGE): 
            self.Kp = Kp
        if(Ki>=0 and Ki<RANGE): 
            self.Ki =Ki
        if(Kd>= 0 and Kd<RANGE):
            self.Kd = Kd 
        self.writefile()
    
    def set_setpoint(self,setpoint): 
        if(setpoint>0 and setpoint<RANGE ): 
            self.setpoint = setpoint
            self.writefile() 
    
    def LoopType(self): 
        if(self.Kp > 0 and self.Ki>0 and self.Kd>0):
            return "PID"
        elif(self.Kp >0 and self.Ki>0): 
            return "PI"
        elif(self.Kp >0 and self.Kd>0): 
            return "PD"
        elif(self.Kp>0): 
            return "P"
        else: 
            return None 


    

class PID(object): 
    def __init__(self, name): 
        self.settings = PID_settings(name)
        self._last_time =  None   
        self._last_output = None
        self._last_input = None
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self.lowrange =  0
        self.highrange = 0 
        self.readsetting()
    


    def readsetting(self): 
        self.settings.readfile()
        print("Read Settings" + str(self.settings.setpoint))


    def setinputrange(self, low, high):
        self.lowrange = low
        self.highrange = high

    
    def calculate_range(self, value):
        percent = (value/ (self.highrange - self.lowrange)) * 100.0
        return percent
    
    def reset(self):
        self._proportional = 0
        self._integral = 0
        self._derivative = 0
        self._integral = _clamp(self._integral, self.settings.min_output, self.settings.max_output)
        self._last_time = None
        self._last_output = None
        self._last_input = None

    
    def changesetpoint(self,setpoint):
        self.settings.set_setpoint(setpoint)
    
    
    def changegain(self,KP, KI, KD):
        self.settings.setgain(KP,KI,KD)
       

    
    def statusprint(self):
        print("PID : Setpoint :  " + str(self.calculate_range(self.settings.setpoint)) + "   Input :  " + str(self._last_input) + "  Output :  " + str(self._last_output))
        print("PID : Kp:  " + str(self._proportional) )
    

    def call(self, input_, dt):
        
         # Compute error termscl
        
        input =  self.calculate_range(input_)
        setpt  = self.calculate_range(self.settings.setpoint)
        #print("PID : Setpoint  :  " + str(self.settings.setpoint) + "   Input :  " + str(input_))
        #print("PID : Setpoint  :  " + str(setpt) + "   Input :  " + str(input) )
        error = setpt - input
        d_input = input - (self._last_input if (self._last_input is not None) else input)


        self._proportional = self.settings.Kp * error 
        # Compute integral and derivative terms
        self._integral += self.settings.Ki * error * dt
        #print("PID : Error   :  " + str(error ) + "   Integral :  " + str(self._integral)  + "   " + str ( self.settings.Ki * error * dt) )
        #self._integral = _clamp(self._integral, self.settings._min_output, self.settings._max_output)  # Avoid integral windup
        self._integral = _clamp(self._integral, -2,  2) 
        self._derivative = -self.settings.Kd * (d_input / dt)

        #print("Propotional " +  str(self._proportional) + "  Integral " + str(self._integral) + "  Derivative  " + str(self._derivative))
        # Compute final output
        output = (self._proportional + self._integral + self._derivative) * -1
        output = _clamp(output, self.settings._min_output, self.settings._max_output)

        # Keep track of state
        self._last_output = output
        self._last_input = input
        #print("PID : Kp :  " + str(self._proportional) + "  Ki :  " + str(self._integral) +  "  Output :  " + str(output))
        #  self._last_time = now
        return output

 
    


'''

tester.writefile() 
tester.readfile()
print(json.dumps(tester.__dict__))
#print(strobj)
#tester = json.loads(strobj)
#tester1 = PID_settings() 
#tester1._init_() 
#tester1 = json.loads(strobj)
#print(tester1)
'''

# import time
# import warnings
# import json 
# class PID_settings(object): 
#     def _init_( 
#         self,
#         Kp=1.0,
#         Ki=0.0,
#         Kd=0.0,
#         setpoint = 0, 
#         sample_time=0.01,
#         output_limits=(None, None),
#         auto_mode=True,
#         error_map=None,
#     ):
#         self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
#         self.setpoint = setpoint
#         self.sample_time = sample_time

#         self._min_output, self._max_output = None, None
#         self._auto_mode = auto_mode
#         self.proportional_on_measurement = proportional_on_measurement
#         self.error_map = error_map

#         self._proportional = 0
#         self._integral = 0
#         self._derivative = 0








# def _clamp(value, limits):
#     lower, upper = limits
#     if value is None:
#         return None
#     elif (upper is not None) and (value > upper):
#         return upper
#     elif (lower is not None) and (value < lower):
#         return lower
#     return value



