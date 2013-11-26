# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 10:57:30 2013

@author: beike
"""
import Chose_Param,fd_mock
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL


class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()        
        self.initUI()
    

        
        
    def initUI(self): 
        
        self.ch_para=Chose_Param.Chose_Param();
        self.but_design=QtGui.QPushButton("text",self)
            
        """
        LAYOUT      
        """
        
        self.layout=QtGui.QGridLayout()
        self.layout.addWidget(self.ch_para)
        self.layout.addWidget(self.but_design)
       
        self.setLayout(self.layout)
        """
        SIGNAL
        """
         
        self.connect(self.but_design,SIGNAL('clicked()'),self.but_press)
        
    def but_press(self):
        """
         ['Least-squares','LP',['Fs','Fpass','Fstop'],[48000,9600,12000],False,True,"tb",["Enter a weight value for each band below",["Wpass","Wstop"],[1,1]]]
        (filtermethode,[[Frequenz_Namen],[Frequenz_Werte]],[Magnitude_Specificationen(je nach dem...)],[Options(je nach dem...)]])
        """
        print "Button clicked"
        # start_busy()
        
        paramlist=[[['Fs','Fpass','Fstop'],[48000,9600,12000]],[["Wpass","Wstop"],[1,1]]]
        filter = fd_mock.fd_1(paramlist)
        # stop_busy()
        #self.plotter.draw(filter)
        
       # items=(self.ch_para.dm.get_FilterMethod,self.ch_para.fs)
        #print self.ch_para.dm.get_FilterMethod()
        #print self.ch_para.fs.get_elm()
        
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Window()
    form.show()
   
    app.exec_()