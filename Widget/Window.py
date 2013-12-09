# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:57:30 2013

@author: beike
"""
import Chose_Param,fd_mock, design_selector, plotter_Hf
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL


class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()        
        self.initUI()     
        
    def initUI(self): 
        
        self.ch_para=Chose_Param.Chose_Param();
        self.but_design=QtGui.QPushButton("DESIGN",self)
        self.pltHf = plotter_Hf.PlotHf() # neu
            
        """
        LAYOUT      
        """
        self.ch_para.setMaximumWidth(250)
        self.layout=QtGui.QGridLayout()
        self.layout.addWidget(self.ch_para,0,0)
        self.layout.addWidget(self.but_design,1,0)
        self.layout.addWidget(self.pltHf,0,1) # neu
       
        self.setLayout(self.layout)
        """
        SIGNAL
        """
         
        self.connect(self.but_design,SIGNAL('clicked()'),self.but_press)
        
    def but_press(self):

        a = self.ch_para.get()
        print "-------------------------"
        print "-------------------------"
        print a
        print "-------------------------"
        print "-------------------------"
        #coeffs = design_selector.select(a)
        #print coeffs[0]
        
       # self.pltHf.pass_param(coeffs)
        #self.pltHf.on_draw()
        # stop_busy()
        # self.plotter.draw(filter)
        
       # items=(self.ch_para.dm.get_FilterMethod,self.ch_para.fs)
        #print self.ch_para.dm.get_FilterMethod()
        #print self.ch_para.fs.get_elm()
        
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Window()
    form.show()
   
    app.exec_()