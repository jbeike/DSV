"""
Auswahl von DesignTyp,FilterMethode 
@author: Julia Beike
Datum:14.11.2013
"""
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

class Design_Method(QtGui.QWidget):
    
    def __init__(self):
        super(Design_Method, self).__init__()        
        self.initUI()
        
        
    def initUI(self): 
        self.design_typ=""
        self.design_filter=""
    
      
        
        self.list_FilterMethod_IIR=["Butterworth","Chebyshev","Elliptic"]

        self.list_FilterMethod_FIR=['Equiripple','Least-squares','Window']
        



        """
        Radio Buttons zur Auswahl des Filtertyps        
        """
       
        
       # self.group.exclusive(True)
        self.radio_FIR=QtGui.QRadioButton("FFT",self)
        self.radio_IIR=QtGui.QRadioButton("IIR",self)
        self.radio_FIR.setChecked(True)
        self.group=QtGui.QButtonGroup()
        self.group.addButton(self.radio_FIR)
        self.group.addButton(self.radio_IIR)
        
        """
        Combobox zur Auswahl des Filtermethode FFT       
        """
        
        self.combo_FilterMethod_FIR=QtGui.QComboBox(self)
        self.combo_FilterMethod_FIR.addItems(self.list_FilterMethod_FIR)

        
        
        """
        Combobox zur Auswahl des Filtermethode IRR       
        """
        
        self.combo_FilterMethod_IIR=QtGui.QComboBox(self)
        self.combo_FilterMethod_IIR.addItems(self.list_FilterMethod_IIR)
     
        
        """
        SIGNALE       
        """

        self.connect(self.combo_FilterMethod_FIR,SIGNAL('activated(QString)'),self.sel_FilterMethod_FIR)

        self.connect(self.combo_FilterMethod_IIR,SIGNAL('activated(QString)'),self.sel_FilterMethod_IIR)
        
        """
        LAYOUT      
        """
        layout_FIR=QtGui.QHBoxLayout()
        layout_FIR.addWidget(self.radio_FIR)
        layout_FIR.addWidget(self.combo_FilterMethod_FIR)
        layout_IIR=QtGui.QHBoxLayout()
        layout_IIR.addWidget(self.radio_IIR)
        layout_IIR.addWidget(self.combo_FilterMethod_IIR)
        layout=QtGui.QGridLayout()
        layout.addWidget(self.radio_FIR,0,0)
        layout.addWidget(self.radio_IIR,1,0)
        layout.addWidget(self.combo_FilterMethod_FIR,0,1)
        layout.addWidget(self.combo_FilterMethod_IIR,1,1)
        self.setLayout(layout)
        
        
    def sel_FilterMethod_FIR(self):
       
   
        self.radio_FIR.setChecked(True)
        
    def sel_FilterMethod_IIR(self):
        
    
        self.radio_IIR.setChecked(True)    
   
 
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Design_Method()
    form.show()
   
    app.exec_()

