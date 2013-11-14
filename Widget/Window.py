# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:21:19 2013
MAINWINDOW

@author: beike
"""
import Design_Method,ResponseType,FilterOrder
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL

class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()        
        self.initUI()
        
        
    def initUI(self): 
   
        self.rs=ResponseType.ResponseType()
        self.dm=Design_Method.Design_Method()
        self.fo=FilterOrder.FilterOrder()
      
        
        """
        LAYOUT      
        """
        
        layout=QtGui.QGridLayout()
        layout.addWidget(self.rs,0,0)
        layout.addWidget(self.dm,1,0)
        layout.addWidget(self.fo,2,0)

        self.setLayout(layout)
        
        
        
   
 
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Window()
    form.show()
   
    app.exec_()


   
        



 