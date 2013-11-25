
"""

Auswahl von DesignTyp,FilterMethode 
@author: Julia Beike
Datum:14.11.2013
"""


import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class Frequency_Specification(QtGui.QWidget):
    
    def __init__(self, lab=[] ,default=[]):
        super(Frequency_Specification, self).__init__()   
        self.lab_namen=lab
        self.labels=[]
        
        self.default_werte=default
        self.textfield=[]
        print self.default_werte
        self.initUI()
        
        
    def initUI(self): 
        anz=len(self.lab_namen)
        i=0
        
        layout=QtGui.QGridLayout()
        self.lab_units=QtGui.QLabel(self)
        self.lab_units.setText("Units")
        self.combo_units=QtGui.QComboBox(self)
        self.combo_units.addItems(["Normalize 0 to 1","Hz","kHz","MHz","GHz"])
        layout.addWidget(self.lab_units,0,0)
        layout.addWidget(self.combo_units,0,1)
        while (i<anz):
        
            self.labels.append(QtGui.QLabel(self))
            self.textfield.append(QtGui.QLineEdit(str(self.default_werte[i])))
            self.labels[i].setText(str(self.lab_namen[i]))
            print self.lab_namen[i]
           
            layout.addWidget(self.labels[i],(i+1),0)
            layout.addWidget(self.textfield[i],(i+1),1)
            i=i+1
            
            
      

 
        self.setLayout(layout)
        
        
    
 
    
if __name__ == '__main__':
    lab=[1,2,3,4,'an','bf']
    default=[1,2,3,4,5,6,7,8,9]
    app = QtGui.QApplication(sys.argv)
    form=Frequency_Specification(lab,default)
    form.show()
   
    app.exec_()
