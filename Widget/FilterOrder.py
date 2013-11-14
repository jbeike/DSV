
"""
Auswahl von DesignTyp,FilterMethode und Window 
@author: juliabeike
Datum:12.11.2013
"""
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class FilterOrder(QtGui.QWidget):
    
    def __init__(self):
        super(FilterOrder, self).__init__()        
        self.initUI()
        
        
    def initUI(self): 
        
   
     
        self.chekManual=QtGui.QRadioButton("Specify Order",self)
        self.chekMinimal=QtGui.QRadioButton("Minimum Order",self)
        self.group =QtGui.QButtonGroup(self)
        self.group.addButton(self.chekManual)
        self.group.addButton(self.chekMinimal)
        self.group.setExclusive(True)
        self.txtManual=QtGui.QLineEdit("10",self)
        self.txtManual.setEnabled(False)

   
        """
        LAYOUT 
        """
        vbox=QtGui.QHBoxLayout()
        vbox.addWidget(self.chekManual)
        vbox.addWidget(self.txtManual)
        layout=QtGui.QVBoxLayout()
        layout.addItem(vbox)
        layout.addWidget(self.chekMinimal)
      
    
        self.setLayout(layout)
        
        

         
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = FilterOrder()
    form.show()
   
    app.exec_()


   
        



 