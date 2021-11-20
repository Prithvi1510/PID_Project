
import math 
from PID import *

class parameter(object):
    def __init__(self, name,type,settable,units):
        self.type = type 
        self.name  = name 
        self.value = 0.0
        self.settable = settable
        self.unitstring = units

    def change_name(self,name): 
            self.name = name 

    def setvalue(self, set_value):
            self.value = set_value


    def getvalue(self): 
            return(self.value) 
        
    def getname(self):

            return(str(self.name))


class model(object):
        def __init__(self):
            self.objectlist = []
            self.name = "Model"
            self.equipment = True 
         

        def addparam(self, variable):
            if(type(variable) == parameter): 
                self.objectlist.append(variable)

        def getvalue(self,paramname): 
            for i in  range(0,len(self.objectlist)): 
                if(self.objectlist[i].name == paramname): 
                    return(self.objectlist[i].value)

            return None

        def setvalue(self,value, paraname):
            
            for i in  range(0,len(self.objectlist)): 
                    #print (self.objectlist[i].name )
                    if(self.objectlist[i].name == paraname):
                        self.objectlist[i].value = value
                        #self.objectlist[i].setvalue(value)

        def get_settable(self): 
            settable_arr = []
            for i in  range(0,len(self.objectlist)): 
                if(self.objectlist[i].settable == True):
                    settable_arr.append(self.objectlist[i].name)
            
            return settable_arr
        
        def print_list_type(self,type_c):
            for i in  range(0,len(self.objectlist)): 
                if(self.objectlist[i].type == type_c): 
                    print(self.objectlist[i].name + " " + self.objectlist[i].value)
        
        def print_list(self):
            for  i in  range(0,len(self.objectlist)): 
                    print(self.objectlist[i].name + " " + str(self.objectlist[i].value))



class tank(model): 
    def __init__(self,name):
        super().__init__() 
        self.name = name
        self.addparam(parameter("Area", "Setting",True, "m2"))
        self.addparam(parameter("Height","Setting", False, 'meters'))
        self.addparam(parameter("Inlet Flow", "Input", False, "m3/sec"))
        self.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
        self.addparam(parameter("Predicted Flow","Setting", False, "m3/sec"))
        self.Quantity = 0
        self.beta = 1.8
        # self.teststart()

    #def teststart(self):
    #    self.setvalue(2,"Inlet Flow")
    #    self.setvalue(5,"Area")
    #    print(self.getvalue("Inlet Flow"))
    

    def start(self):
        x = self.getvalue("Area")
        self.setvalue(self.Quantity /x, "Height")

    def update_model(self): 
        new_flow = self.beta * math.sqrt(self.getvalue("Height"))
        self.setvalue(new_flow,"Predicted Flow")
        #print(self.getvalue("Predicted Flow"))


    def compute(self,timeslice):   
        delta =  (self.getvalue("Inlet Flow") -  self.getvalue("Outlet Flow")) * timeslice
        self.Quantity = self.Quantity +  delta
        #print(self.getvalue("Inlet Flow"))
        #print(self.getvalue("Outlet Flow"))
        #print(" Quantity " +  str(self.Quantity) + " Delta  " + str(delta))
        #print("Inlet flow : " + str(self.getvalue("Inlet Flow")) +" " +  str(self.getvalue("Outlet Flow")))
        
        x = self.getvalue("Area")
        self.setvalue(self.Quantity /x, "Height")
       

    def statusprint(self):
        print("Inlet Flow : "  + str(self.getvalue("Inlet Flow")) +  "Quantity : " + str(self.Quantity))
        print(" Height : " + str(self.getvalue("Height")) + "Outlet Flow : " + str(self.getvalue("Outlet Flow")))
         


class Pipe(model): 
    def __init__(self,name):
        super().__init__() 
        self.name = name
        self.addparam(parameter("Inlet Flow", "Input", True, "m3/sec"))
        self.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
        self.equipment = False
        self.teststart()
    
    def teststart(self): 
        self.setvalue(2,"Inlet Flow")


    def start(self):
        x = self.getvalue("Inlet Flow")
        self.setvalue(x, "Outlet Flow")

    def compute(self, timeslice):
        x = self.getvalue("Inlet Flow")
        self.setvalue(x, "Outlet Flow")
   
    def statusprint(self):
        print("Pipe : Inlet Flow : "  + str(self.getvalue("Inlet Flow")) +  "Outlet Flow : " + str(self.getvalue("Outlet Flow")))
    


        
class Pipewithvalve(model): 
    def __init__(self,name):
        super().__init__() 
        self.name = name 
        self.addparam(parameter("Inlet Flow", "Input", True, "m3/sec"))
        self.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
        self.addparam(parameter("ControlValveSetting","Settable", True, "%"))
        self.equipment = False

    def start(self):
        x = self.getvalue("Inlet Flow")
        y  = self.getvalue("ControlValveSetting")
        self.setvalue(x * (y/100), "Outlet Flow")

       
    def compute(self,timeslice):
        x =  self.getvalue("Inlet Flow")
        y  = self.getvalue("ControlValveSetting")
        self.setvalue(x * (y/100), "Outlet Flow")
        #print( "Valve Setting  " + str( y)+  str(self.getvalue("Outlet Flow")) )

    def statusprint(self, timeslice):
        print("Pipe with Control : Inlet Flow : "  + str(self.getvalue("Inlet Flow")) +  "Outlet Flow : " + str(self.getvalue("Outlet Flow")))
        print("Valve Output Set  : "  + str(self.getvalue("ControlValveSetting")))


















  
# class parameter(object):
#     def __init__(self, name,type,settable,units):
#         self.type = type 
#         self.name  = name 
#         self.value = 0 
#         self.settable = settable
#         self.unitstring = units

#     def change_name(self,name): 
#             self.name = name 

#     def setvalue(self, set_value):
#             self.value = set_value


#     def getvalue(self): 
#             return(self.value) 
        
#     def getname(self):
#             return(str(self.name))

        

# class model(object):
#         def __init__(self):
#             self.objectlist = []
#             self.name = "Model"
#             self.equipment = True 
         

#         def addparam(self, variable):
#             if(type(variable) == parameter): 
#                 self.objectlist.append(variable)

#         def getvalue(self,paramname): 
#             for i in  range(0,len(self.objectlist)): 
#                 if(self.objectlist[i].name == paramname): 
#                     return(self.objectlist[i].value)

#             return None

#         def setvalue(self,value, paraname):
            
#             for i in  range(0,len(self.objectlist)): 
#                     print (self.objectlist[i].name )
#                     if(self.objectlist[i].name == paraname):
#                         self.objectlist[i].value = value
#                         #self.objectlist[i].setvalue(value)

#         def get_settable(self): 
#             settable_arr = []
#             for i in  range(0,len(self.objectlist)): 
#                 if(self.objectlist[i].settable == True):
#                     settable_arr.append(self.objectlist[i].name)
            
#             return settable_arr
        
#         def print_list_type(self,type_c):
#             for i in  range(0,len(self.objectlist)): 
#                 if(self.objectlist[i].type == type_c): 
#                     print(self.objectlist[i].name + " " + self.objectlist[i].value)
        
#         def print_list(self):
#             for  i in  range(0,len(self.objectlist)): 
#                     print(self.objectlist[i].name + " " + str(self.objectlist[i].value))

 
 

# class tank(model): 
#     def __init__(self,name):
#         super().__init__() 
#         self.name = "Tank"
#         self.model.addparam(parameter.__init__("Area", "Setting", 0, True, "m2"))
#         self.model.addparam(parameter.__init__("Height","Setting", 0, False, 'meters'))
#         self.model.addparam(parameter.__init__("Inlet Flow", "Input", 0, False, "m3/sec"))
#         self.model.addparam(parameter.__init__("Outlet Flow","Output", 0, False, "m3/sec"))
#         self.Quantity = 0

#     def start(self):
#         x = self.getvalue("Area")
#         self.setvalue(self.Quantity/x, "Height")

#     def compute(self):
#         Quantity = self.getvalue("Inlet Flow") -  self.getvalue("Outlet Flow")
#         x = self.getvalue("Area")
#         self.setvalue(Quantity/x, "Height")
      
      
 
# class tank(model): 
#     def __init__(self,name):
#         super().__init__() 
#         self.name = name
#         self.addparam(parameter("Area", "Setting",True, "m2"))
#         self.addparam(parameter("Height","Setting", False, 'meters'))
#         self.addparam(parameter("Inlet Flow", "Input", False, "m3/sec"))
#         self.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
#         self.Quantity = 0

#     def start(self):
#         x = self.getvalue("Area")
#         self.setvalue(self.Quantity/x, "Height")

#     def compute(self):
#         Quantity = self.getvalue("Inlet Flow") -  self.getvalue("Outlet Flow")
#         x = self.getvalue("Area")
#         self.setvalue(self.Quantity /x, "Height")
        

        
# class Pipe(model): 
#     def __init__(self,name):
#         super().__init__() 
#         self.name = name
#         self.model.addparam(parameter("Inlet Flow", "Input", True, "m3/sec"))
#         self.model.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
#         self.equipment = False

#     def start(self):
#         x = self.getvalue("Inlet Flow")
#         self.setvalue(x, "Outlet Flow")

#     def compute(self):
#         x = self.getvalue("Inlet Flow")
#         self.setvalue(x, "Outlet Flow")
    

        
        
# class Pipewithvalve(model): 
#     def __init__(self,name):
#         super().__init__() 
#         self.name = name 
#         self.model.addparam(parameter("Inlet Flow", "Input", True, "m3/sec"))
#         self.model.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
#         self.model.addparam(parameter("ControlValveSetting","Settable", True, "%"))
#         self.equipment = False

#     def start(self):
#         x = self.getvalue("Inlet Flow")
#         y  = self.getvalue("ControlValveSetting")
#         self.setvalue(x * (y/100), "Outlet Flow")

#     def compute(self):
#         x = self.getvalue("Inlet Flow")
#         y  = self.getvalue("ControlValveSetting")
#         self.setvalue(x * (y/100), "Outlet Flow")








# tank1 = tank("dasd") 
# tank1.print_list()
# newparam = parameter("Area", "Setting",True, "m2")
# newparam.setvalue(12)
# print(newparam.value)
# model1 = model()
# model1.addparam(parameter("Area", "Setting",True, "m2"))
# model1.addparam(parameter("Height","Setting", False, 'meters'))
# model1.setvalue(24,"Area")
# print(model1.getvalue("Area"))
# model1.setvalue(245,"Area")
# print(model1.getvalue("Area"))
# tank1 = tank("tank121")
# #print(tank1.objectlist)
# tank1.objectlist[0].setvalue(10)
# tank1.objectlist[2].setvalue(39)
# tank1.objectlist[3].setvalue(23)
# tank1.compute()
# print(tank1.Quantity)
# print(tank1.objectlist[1].value)
# tank1.start()
# print(tank1.objectlist[1].value) 

 

# We write a simulator
# create inlet , tank, outler
# set clock, set time step =  .1 sec
# set connection --  pipe outler flow  - set parameter
#                    tnk outlet - to p outlet pile
#                    the otflow has interlock


# class model(object):
#     def __init__(self):
#         self.model_dictionary = {}
#         self.tank_id = 1 
#         self.interconnect_id = 1  
    
#     def addparam(self,__object):
#         if(type(__object) == tank ): 
#             tank_string = "tank" + str(self.tank_id)
#             self.model_dictionary[tank_string] = __object
#             self.tank_id = self.tank_id + 1
#         elif(type(__object) == interconnect):
#             interconnect_string = "inter" + str(self.interconnect_id)
#             self.model_dictionary[interconnect_string] = __object
#             self.interconnect_id = self.interconnect_id + 1 

#         else: 
#             return None

#     def deleteparam(self,dict_key):
#         if dict_key in self.model_dictionary:
#             self.model_dictionary.pop(dict_key)

#     def viewcomponents(self):
#         list1 = self.model_dictionary.keys()
#         print(list1)

    
            
 
#     In a simulator, we have equipments and interconnection
#     The euipments and interconnection vary from what we want to model
#     So both equipment and interconnection will have input variables, output variables and setting variables
#     The number of each depends on type of equipment or ConnectionAbortedError

#     First is get a base class
#     base class for model
#     - is it an equipment or interconnection - type
#       input array of floating number, you can slso


#       So to manager all this creatr mofrl

#       it has an array of dictonary
#       dictory object is name: string, value- Float no, type = input, output or PID_settings
#       =Method  - Addparameter - it add a dictonaru to array, remove param given  a name
#       get value given a name - getvalue(name: string)
#       set value = (name: string, value which is no)
#       getvalues( array of names) get an array of ValuesView
#       simiarly for set

#       two empy methods, init and compute


# class tank(object):
#     def __init_(self):
#         self.area = 0 
#         self.name = " default_tank"

# class interconnect(object):
#     def __init__(self):  
#         self.flow = 0 
#         self.name = " defaultinterconnect" 




# #tests
# tank1 = tank() 
# tank1.__init__()
# print(tank1)
# tank2 = tank() 
# tank2.__init__()
# print(type(tank2))

# #interconnect1 = interconnect.__init__()
# interconnect1 = interconnect()
# interconnect1.__init__()
# model1 = model()
# model1.__init__() 
# print(model1.tank_id)
# print(model1.model_dictionary)

# model1.addparam(tank1)
# model1.addparam(tank2) 
# model1.addparam(interconnect1)
# model1.deleteparam("inter1")
