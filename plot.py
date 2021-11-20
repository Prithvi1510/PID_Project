from PyQt5.QtCore import QSize, Qt, QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import (QApplication,  
                             QPushButton, 
                             QDoubleSpinBox,
                             QWidget ,
                             QMainWindow ,
                             QHBoxLayout,
                             QVBoxLayout,
                             QLabel,
                             QFormLayout) 
import sys
import os 
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QColor, QPalette

import pyqtgraph as pg 
from pyqtgraph import PlotWidget, plot
from simulator import *

ApplyObject = {}

cases = 1000
quantity = 60

class Worker(QRunnable):
    def __init__(self): 
            super().__init__()
            self.simulate = simulator(0.1) 
            #self.simulate.simulate_init(quantity)
            ApplyObject["KP"] = self.simulate.Controller.settings.Kp
            ApplyObject["KI"] = self.simulate.Controller.settings.Ki
            ApplyObject["KD"] = self.simulate.Controller.settings.Kd
            ApplyObject["Set"] = self.simulate.Controller.settings.setpoint
            ApplyObject["IF"] = self.simulate.inletflow
            self.testcases_run = cases
            self.timeaxis = []
            self.levelaxis = []
            self.setpointaxis = []
            self.ifaxis =[]
            self.done = False
            self.signals = WorkerSignals()
            self.tempvalue = 60
            
          
    
 
    #@pyqtSlot()
    def run(self):
            self.simulate.simulate_init(self.tempvalue)
            print("Entered Run  $$$$$$$$$$$$$$$$")
            print(self.simulate.tank1.Quantity)
            init = self.testcases_run
            while( self.testcases_run): 
                self.testcases_run -= 1
                self.simulate.simulate_step()
                if(self.testcases_run % 10 == 0):
                    self.timeaxis.append( (init - self.testcases_run) * 0.1)
                    self.levelaxis.append(self.simulate.controlledvalue)
                    self.setpointaxis.append(self.simulate.Controller.settings.setpoint)
                    self.ifaxis.append(self.simulate.inletflow)
                    
                self.simulate.setcontrol()
                if(self.simulate.debug == True) :
                    self.simulate.simulate_print(self.testcases_run) 
           
            self.done = True
        
            self.signals.finished.emit()
            self.signals.result.emit({"CV": self.simulate.outletpipe.getvalue("ControlValveSetting"), "Height": self.simulate.controlledvalue, "Q":self.simulate.tank1.Quantity })
           
            #give some things here... and reenable apply - so we can signal
   
    def reinit(self, Kp, Ki, Kd, Inlet, Set):
            self.done = False
            self.testcases_run = cases
            self.timeaxis = []
            self.levelaxis = []
            self.setpointaxis = []
            self.ifaxis =[]
            self.simulate.simulate_reinit(Kp,Ki,Kd,Inlet, Set)

    
    
     


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(dict)


class MainWindow(QMainWindow):

    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Simulator")
        self.setFixedSize(QSize(1000,700))
 
        self.plabel = QtWidgets.QLabel()   
        canvas = QtGui.QPixmap(os.getcwd() + '/Level.png')
        self.plabel.setPixmap(canvas)
        
        
        self.leftlayout = QVBoxLayout()
        self.rightlayout  = QVBoxLayout() 
        self.mainlayout = QHBoxLayout() 
        self.leftmiddlelayout = QHBoxLayout()
        self.leftbottomlayout = QHBoxLayout()
        

        self.Levellabel = QLabel("Level   meters")
        self.Arealabel = QLabel("Tank Area  meter2")
        self.OutletFlowlabel = QLabel("FlowOut meter/sec")
        self.ControlValveSettinglabel = QLabel("Valve Open %") 
        self.leftmiddle1layout = QVBoxLayout()
        self.leftmiddle1layout.addWidget(self.Levellabel)
        self.leftmiddle1layout.addWidget(self.Arealabel)
        self.leftmiddle1layout.addWidget(self.OutletFlowlabel)

        self.leftmiddle2layout = QVBoxLayout()
        self.leftmiddle2layout.addWidget(self.ControlValveSettinglabel)
        self.leftmiddlelayout.addLayout(self.leftmiddle1layout)
        self.leftmiddlelayout.addLayout(self.leftmiddle2layout)
        


        #PID SETTINGS
        form = QFormLayout()
        self.kplabel = QDoubleSpinBox()
        self.kplabel.setRange(0,10)
        self.kplabel.setSingleStep(0.1)
        self.kilabel  = QDoubleSpinBox() 
        self.kilabel.setRange(0,100)
        self.kilabel.setSingleStep(0.1)
        self.kdlabel = QDoubleSpinBox() 
        self.kdlabel.setRange(0,10)
        self.kdlabel.setSingleStep(0.1)
        self.SettingButton = QPushButton("Apply")
        self.SettingButton.setEnabled(True)
        form.addRow(QLabel("Kp"),self.kplabel)
        form.addRow(QLabel("Ki"),self.kilabel)
        form.addRow(QLabel("Kd"),self.kdlabel)
        form.addRow(self.SettingButton)
        self.SettingButton.clicked.connect(self.apply_button_clicked)

        #disturbances 
        form2 = QFormLayout()
        self.qflow =QDoubleSpinBox() 
        self.qflow.setRange(0,10)
        self.qflow.setSingleStep(0.1)
        self.changeSp = QDoubleSpinBox() 
        self.changeSp.setRange(0,10)
        self.changeSp.setSingleStep(0.1)
        form2.addRow(QLabel("Q Flow:"),self.qflow)
        form2.addRow(QLabel("Change setpoint:"),self.changeSp)
       
        self.leftbottomlayout.addLayout(form)
        self.leftbottomlayout.addLayout(form2)
    
        self.leftlayout.addWidget(self.plabel)
        self.leftlayout.addLayout(self.leftmiddlelayout)
        self.leftlayout.addLayout(self.leftbottomlayout)
        
       #self.leftlayout.addWidget(self.canvas)   
    
    
    
        #plots 1cls

        self.spGraph = pg.PlotWidget()
        self.spGraph.setBackground("k")
        self.spGraph.setTitle("Setpt Change")
         
        self.spGraph.setLabel('bottom', 'Time Sec')
        self.spGraph.setLabel('left', 'Level meter')
        self.spGraph.showGrid(x = True, y = True)
        self.spGraph.setGeometry(100, 100, 300,300)
        

        #plot2 s
        self.mvGraph = pg.PlotWidget()
        self.mvGraph.setBackground("k")
        self.mvGraph.setTitle("Response to MV Changes")
        self.mvGraph.setLabel('bottom', 'Time 0.1 sec')
        self.mvGraph.setLabel('left', 'Inlet Flow')
        self.mvGraph.setLabel('right', 'Level')
        self.mvGraph.showGrid(x = True, y = True)
        self.mvGraph.setGeometry(100, 100, 300,300)
        

        self.rightlayout.addWidget(self.spGraph)
        self.rightlayout.addWidget(self.mvGraph)
        self.mainlayout.addLayout(self.leftlayout)
        self.mainlayout.addLayout(self.rightlayout)
        
                
        widget = QWidget()
        widget.setLayout(self.mainlayout)
        self.setCentralWidget(widget)
        self.mwtemp = 0
        self.threadpool = QThreadPool()
        self.worker = Worker()
        self.applyform()
        self.worker.signals.finished.connect(self.worker_complete) 
        self.worker.signals.result.connect(self.worker_output)
        self.threadpool.start(self.worker)


    def applyform(self):
        self.kplabel.setValue( ApplyObject["KP"])
        self.kilabel.setValue( ApplyObject["KI"])
        self.kdlabel.setValue( ApplyObject["KD"])
        self.qflow.setValue( ApplyObject["IF"])
        self.changeSp.setValue( ApplyObject["Set"])
        
 
    
    def apply_button_clicked(self):
        print("Apply Clicked")
        KP = self.kplabel.value( )
        KI = self.kilabel.value( )
        KD = self.kdlabel.value( )
        IF = self.qflow.value( )
        Sepoint = self.changeSp.value(  ) 
        self.worker = Worker()
        self.worker.reinit(KP, KI, KD, IF, Sepoint)
        self.worker.signals.finished.connect(self.worker_complete) 
        self.worker.signals.result.connect(self.worker_output)
        self.worker.tempvalue = self.mwtemp
        #print("REINIT PARAMETERS")
        #print(KP, KI, KD, IF, Sepoint)
        self.threadpool.start(self.worker)

    def worker_complete(self):
        pen3 = pg.mkPen(color = (255,0,0))
        pen4 = pg.mkPen(color = (0,127,127))
        pen1 = pg.mkPen(color = (0,255,0))
        pen2 = pg.mkPen(color = (0,127,127))
       
        print("Completed")
        #print(self.worker.timeaxis)
        #print(self.worker.levelaxis)
        #print(self.worker.setpointaxis)
        #print(self.worker.ifaxis)

        self.spGraph.setYRange(0,8,0)
        self.spGraph.setXRange(0,120,0)
        self.mvGraph.setYRange(0,8,0)
        self.mvGraph.setXRange(0,120,0)

        self.spGraph.clear()
        self.mvGraph.clear()

        self.spGraph.plot(self.worker.timeaxis,self.worker.levelaxis,pen = pen1)
        self.spGraph.plot(self.worker.timeaxis,self.worker.setpointaxis,pen =pen2)
        self.mvGraph.plot(self.worker.timeaxis,self.worker.levelaxis,pen =pen4)
        self.mvGraph.plot(self.worker.timeaxis,self.worker.ifaxis,pen =pen3)

  

    
    def worker_output(self, s):
        print("xx  output")
        self.mwtemp = s['Q']
        temp1 = s['Height']
        temp2 = s['CV']
        self.Levellabel.setText("Level  " + str(temp1)  + "  meters")
        self.Arealabel.setText("Tank Area 12 meter2")
        self.OutletFlowlabel.setText("FlowOut meter/sec")
        self.ControlValveSettinglabel.setText("Valve Open  " + str(temp2) + "  %") 
        
    
       


        #self.signals.result.emit({"CV": self.simulate.outletpipe.getvalue("ControlValveSetting"), "Height": self.simulate.controlledvalue, "Q":self.simulate.tank1.Quantity })
           


    #    need to update values in simulator 
    #    run it again for x secs - ie start worker ...
    #    so put the worker start in another function, and also until runs do not allow apply
        

    #def runworker(self)
    #    self.threadpool.start(worker)
    #    in runner enable apply only after
        


app = QApplication(sys.argv)
window = MainWindow() 
window.show() 
app.exec_()



#get the values and fill the store , so before application start fill up the windows
#Kp. Ki Kd  and also set up the disturbance flow - input flow, xxx
# at end of 100 loop set graph - update, stop and go. Every apply trigger the output
# check apply, signal -  loop takes value and does about 120 run and then updates screen
#simulate = simulator(0.1) 
#simulate.simulate_init()
#testcases = 1500
#while(testcases): 
#  testcases -= 1
#  simulate.simulate_step()
#  simulate.setcontrol()
#  if(simulate.debug == True) :
#       simulate.simulate_print(testcases)





















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
#                     #print (self.objectlist[i].name )
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
#         self.name = name
#         self.addparam(parameter("Area", "Setting",True, "m2"))
#         self.addparam(parameter("Height","Setting", False, 'meters'))
#         self.addparam(parameter("Inlet Flow", "Input", False, "m3/sec"))
#         self.addparam(parameter("Outlet Flow","Output", False, "m3/sec"))
#         self.addparam(parameter("Predicted Flow","Setting", False, "m3/sec"))
#         self.Quantity = 0
#         self.beta = 0.5

#     def start(self):
#         x = self.getvalue("Area")
#         self.setvalue(self.Quantity /x, "Height")

#     def update_model(self):
#         self.setvalue(self.beta * sqrt (self.getvalue("Height")), "PredictedOutletflow")

#     def compute(self):    
#         self.Quantity = self.getvalue("Inlet Flow") -  self.getvalue("Outlet Flow")
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




# tank1      = tank("tank1")
# tank1.setvalue(5, "Area")
# inletpipe  = Pipe("Inlet pipe")
# outletpipe = Pipewithvalve("Outlet pipe")
# inletpipe = Pipe.setvalue(6,"Inlet Flow")

# timeslice = 0.1
# time = 0.0

# def simulate():
#     inletpipe.compute()
#     tank1.setvalue(inletpipe.getvalue("Outlet Flow"), "Inlet Flow")
#     tank1.update_model()
#     outletpipe.setvalue(tank1.getvalue("PredictedOutletflow"), "Inlet Flow")
#     outletpipe.compute()
#     tank1.setvalue(outletpipe.getvalue("Outlet Flow"), "Outlet Flow")
#     tank1.compute()
#     time = time + timeslice








'''
Area", "Setting",True, "m2"))
        self.addparam(parameter("Height","Setting", False, 'meters'))
        self.addparam(parameter("Inlet Flow", "Input", False, "m3/sec"))
        self.addparam(parameter("Outlet Flow
'''

'''
tank1 = tank("tank121")
#print(tank1.objectlist)
tank1.objectlist[0].setvalue(10)
tank1.objectlist[2].setvalue(39)
tank1.objectlist[3].setvalue(23)
tank1.compute()
print(tank1.Quantity)
print(tank1.objectlist[1].value)
tank1.start()
print(tank1.objectlist[1].value) 

'''




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


#model1.print_list()



# from PyQt5.QtCore import QSize, Qt, left 
# from PyQt5.QtWidgets import (QApplication, QWidget , QMainWindow ,QGridLayout,QHBoxLayout,QVBoxLayout,QLabel) 
# import sys 
# from PyQt5.QtGui import QColor, QPalette
# from simulator import *

# class Color(QWidget):
#     def __init__(self, color):
#         super().__init__()
#         self.setAutoFillBackground(True)
#         palette = self.palette()
#         palette.setColor(QPalette.Window, QColor(color))
#         self.setPalette(palette)

# class MainWindow(QMainWindow):
#     def __init__(self): 
#         super().__init__()
#         self.setWindowTitle("Simulator")
#         self.setFixedSize(QSize(800,600))
#         self.pagelayout = QHBoxLayout()
#         self.leftlayout = QVBoxLayout()
#         self.leftbottomlayout = QHBoxLayout()
#         self.rightlayout  = QVBoxLayout() 
#         self.lbl1 = QVBoxLayout() 
#         self.lbl2 = QVBoxLayout()
#         self.lbl3 = QVBoxLayout() 
#         self.pagelayout.addLayout(self.leftlayout)
#         self.pagelayout.addLayout(self.rightlayout)
#         self.leftlayout.addLayout(self.leftbottomlayout)
#         self.leftbottomlayout.addLayout(self.lbl1)
#         self.leftbottomlayout.addLayout(self.lbl2)
#         self.leftbottomlayout.addLayout(self.lbl3)
#         self.kp_label = QLabel(); 
#         self.ki_label = QLabel(); 
#         self.kd_label = QLabel();  

#         #
#         self.leftbottomlayout.addWidget(Color("Green"))
#         self.lbl1.addWidget(Color("Blue"))
#         self.lbl2.addWidget(Color("Yellow"))
#         self.lbl3.addWidget(Color("Purple"))
#         self.leftlayout.addWidget(Color("Red"))
#         self.rightlayout.addWidget(Color("Cyan"))

#         widget = QWidget()
#         widget.setLayout(self.pagelayout)
#         self.setCentralWidget(widget)





# app = QApplication(sys.argv)
# window = MainWindow() 
# window.show() 
# app.exec_()
