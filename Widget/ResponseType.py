
"""
Auswahl von DesignTyp,FilterMethode und Window 
@author: juliabeike
Datum:12.11.2013
"""

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class ResponseType(QtGui.QWidget):
    
    def __init__(self):
        super(ResponseType, self).__init__()        
        self.initUI()
        
        
    def initUI(self): 
        



        """
        Radio Buttons zur Auswahl des REsponse Type        
        """


       # self.group.exclusive(True)
        self.radio_HP=QtGui.QRadioButton("Highpass",self)
        self.radio_LP=QtGui.QRadioButton("Lowpass",self)
        self.radio_BP=QtGui.QRadioButton("Bandpass",self)
        self.radio_BS=QtGui.QRadioButton("Bandstop",self)
        self.radio_HP.setChecked(True)
        self.group=QtGui.QButtonGroup()
        self.group.addButton(self.radio_HP)
        self.group.addButton(self.radio_LP)
        self.group.addButton(self.radio_BP)
        self.group.addButton(self.radio_BS)
        
        """
        LAYOUT      
        """
        
        layout=QtGui.QGridLayout()
        layout.addWidget(self.radio_HP,0,0)
        layout.addWidget(self.radio_LP,1,0)
        layout.addWidget(self.radio_BP,2,0)
        layout.addWidget(self.radio_BS,3,0)
      
        self.setLayout(layout)
        
 
         
    def  get(self):
        """
        Rückgabe des aktuellen Filtertyps
        """
        if (self.radio_HP.isChecked()==True):
            return "HP"
        elif (self.radio_LP.isChecked()==True):
            return "LP"
        elif (self.radio_BP.isChecked()==True):
            return "BP"
        else :
            return "BS"  

          
            
   
 
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = ResponseType()
    
    form.show()
    i=form.get_selected_button()
    print i
    app.exec_()


   
        



 