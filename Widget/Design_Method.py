
"""
Created on Fri Nov 08 12:52:10 2013

@author: Acer
"""
import sys
from PyQt4 import QtGui

class Design_Method(QtGui.QWidget):
    
    def __init__(self):
        super(Design_Method, self).__init__()        
        self.initUI()
        
        
    def initUI(self): 
        self.design_typ=""
        self.design_filter=""
        list_IIR=['ellip','cheby1','cheby2','butter','bessel']
        list_FIR=['WIN','WIN2','REMEZ','MANUAL']
        self.rbut_IIR=QtGui.QRadioButton("IIR",self)
        self.rbut_FIR=QtGui.QRadioButton("FIR",self)
        
        self.combo_IIR=QtGui.QComboBox(self)
        self.combo_IIR.addItems(list_IIR)
        self.combo_FIR=QtGui.QComboBox(self)
        self.combo_FIR.addItems(list_FIR)
        self.group = QtGui.QButtonGroup()
        self.group.addButton(self.rbut_IIR)
        self.group.addButton(self.rbut_FIR)       
        self.group.setExclusive(True)
        self.rbut_IIR.clicked.connect(self.checkt_IIR)
        self.rbut_FIR.clicked.connect(self.checkt_FIR)
        hbox1=QtGui.QHBoxLayout()
        hbox1.addWidget(self.rbut_IIR)
        hbox1.addWidget(self.combo_IIR)
        
        hbox2=QtGui.QHBoxLayout()
        hbox2.addWidget(self.rbut_FIR)
        hbox2.addWidget(self.combo_FIR)
        mainBox=QtGui.QVBoxLayout()
        mainBox.addItem(hbox1)
        mainBox.addItem(hbox2)
       
        self.setLayout(mainBox)
    def checkt_FIR(self):
        print "checked: FIR"  
        self.design_typ="FIR"
        self.combo_IIR.setHidden(True)
        self.combo_FIR.setHidden(False)
        self.getFIR_IIR()
    def checkt_IIR(self):
          
        print "checked: IIR"
        self.design_typ="IIR"
        self.combo_FIR.setHidden(True)
        self.combo_IIR.setHidden(False)
        self.getFIR_IIR()
    def getFIR_IIR(self):
        
       if self.design_typ=="FIR":
            self.design_filter=self.combo_FIR.currentText()
       if self.design_typ=="IIR":
            self.design_filter=self.combo_IIR.currentText()
       return self.design_filter,self.design_typ
        
         
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Design_Method()
    form.show()
    app.exec_()


   
        



 