
"""
Auswahl von DesignTyp,FilterMethode und Window 
@author: juliabeike
Datum:12.11.2013
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
    
      
        self.list_DesignType=["IIR","FIR"]
        self.list_FilterMethod_IIR=["PY_DESIGN","MANUAL"]
        self.list_FilterWindow_IIR=['ellip','cheby1','cheby2','butter','bessel']
        self.list_FilterMethod_FIR=['WIN','WIN2','REMEZ','MANUAL']
        self.list_FilterWindow_FIR=['boxcar', 'hann', 'bartlett', 'nuttall']



        """
        Combobox zur Auswahl des Filtertyps        
        """
        self.combo_DesignType=QtGui.QComboBox(self)
        self.combo_DesignType.addItems(self.list_DesignType)
        
        
        
        """
        Combobox zur Auswahl des Filtermethode       
        """
        
        self.combo_FilterMethod=QtGui.QComboBox(self)
        self.combo_FilterMethod.addItems(self.list_FilterMethod_IIR)
        self.combo_FilterMethod.setEnabled(False)
        
        """
        Combobox zur Auswahl des Window       
        """
        
        self.combo_FilterWindow=QtGui.QComboBox(self)
        self.combo_FilterWindow.addItems(self.list_FilterWindow_IIR)
        self.combo_FilterWindow.setVisible(False)

        """
        SIGNALE       
        """

        self.connect(self.combo_DesignType,SIGNAL('activated(QString)'),self.sel_DesignType)
        self.connect(self.combo_FilterMethod,SIGNAL('activated(QString)'),self.sel_FilterMethod)
        
        """
        LAYOUT      
        """
        layout=QtGui.QVBoxLayout()
        layout.addWidget(self.combo_DesignType)
        layout.addWidget(self.combo_FilterMethod)
        layout.addWidget(self.combo_FilterWindow)       
    
        self.setLayout(layout)
        
        
    def sel_DesignType(self):
        text=self.combo_DesignType.currentText()
        print text
        if text=="IIR":
            self.combo_FilterMethod.clear()
            self.combo_FilterMethod.addItems(self.list_FilterMethod_IIR)
            self.combo_FilterMethod.setEnabled(True)
        if text=="FIR":
            self.combo_FilterMethod.clear()
            self.combo_FilterMethod.addItems(self.list_FilterMethod_FIR)
            self.combo_FilterMethod.setEnabled(True)
        
        self.combo_FilterWindow.setVisible(False)
   
 
    def sel_FilterMethod(self):
        text=self.combo_FilterMethod.currentText()
        print text
   
        if text=="PY_DESIGN":
            self.combo_FilterWindow.clear()
            self.combo_FilterWindow.addItems(self.list_FilterWindow_IIR)
            self.combo_FilterWindow.setVisible(True)
        elif text=='WIN2'or text=='WIN':
            self.combo_FilterWindow.clear()
            self.combo_FilterWindow.addItems(self.list_FilterWindow_FIR)
            self.combo_FilterWindow.setVisible(True)
        else:
            #print "Unsichtbar"
            self.combo_FilterWindow.setVisible(False)
  
  
         
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Design_Method()
    form.show()
    app.exec_()


   
        



 