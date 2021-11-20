import os
from PID import * 
from modelobject import * 


class simulator(object):
    def __init__(self,timestep):
        self.timeslice = 0.1
        self.timestep = timestep
        self.tank1 = tank("Tank1")
        self.inletpipe = Pipe("Inlet Pipe")
        self.outletpipe = Pipewithvalve("Outlet Pipe")
        self.Controller = PID("Level Controller")
        self.debug = False  
        self.inletflow = 1.5   
        self.controlledvalue = 0    

    def simulate_init(self, quant):
        self.tank1.setvalue(12, "Area")
        self.tank1.Quantity = quant
        print("&&&&&&&&&&&&&&&&&&")
        print(self.tank1.Quantity)
        print(quant)
        self.inletpipe.setvalue(self.inletflow  , "Inlet Flow")
        #self.outletpipe.setvalue(50, "ControlValveSetting")
        self.Controller.setinputrange( 0 , 8)
    
    def simulate_reinit(self, KP, KI, KD, IF, Sepoint):
        self.inletflow = IF 
        self.inletpipe.setvalue(self.inletflow  , "Inlet Flow")
        self.Controller.changesetpoint(Sepoint)
        self.Controller.changegain(KP, KI, KD)

     

    def simulate_step(self):
        self.inletpipe.compute(self.timeslice)
        self.tank1.setvalue(self.inletpipe.getvalue("Outlet Flow"), "Inlet Flow")
        self.tank1.update_model()
        self.outletpipe.setvalue(self.tank1.getvalue("Predicted Flow"), "Inlet Flow")
        self.outletpipe.compute(self.timeslice)
        self.tank1.setvalue(self.outletpipe.getvalue("Outlet Flow"), "Outlet Flow")
        self.tank1.compute(self.timeslice)
        self.timestep += self.timeslice
       

    def setcontrol(self):
        feedback = self.tank1.getvalue("Height")
        self.controlledvalue = feedback   
        self.outletpipe.setvalue(self.Controller.call(feedback, self.timeslice),  "ControlValveSetting")

    
    def simulate_print(self, testcaseno):
        print("*************** Loop  " +  str(testcaseno) + "**************" )
        # self.inletpipe.statusprint()
        # self.tank1.statusprint()
        #self.Controller.statusprint()
        # self.outletpipe.statusprint()
        #print("*****************************************************   ")
        

#simulate = simulator(0.1) 
#simulate.simulate_init()
#testcases = 1500
#while(testcases): 
#  testcases -= 1
#  simulate.simulate_step()
#  simulate.setcontrol()
#  if(simulate.debug == True) :
#       simulate.simulate_print(testcases)