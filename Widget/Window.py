# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:21:19 2013
MAINWINDOW

@author: beike
"""
import Design_Method,ResponseType,FilterOrder,Frequency_Specification
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
        self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fpass','Fstop'],[48000,9600,12000])
        
        """
        LAYOUT      
        """
        
        self.layout=QtGui.QGridLayout()
        self.layout.addWidget(self.rs,0,0)
        self.layout.addWidget(self.dm,1,0)
        self.layout.addWidget(self.fo,2,0)
        self.layout.addWidget(self.fs,3,0)

        self.setLayout(self.layout)
        """
        SIGNAL
        """
         
        self.connect(self.dm.combo_FilterMethod_FIR,SIGNAL('activated(QString)'),self.chose_design_methode)
        self.connect(self.dm.combo_FilterMethod_IIR,SIGNAL('activated(QString)'),self.chose_design_methode)
        self.connect(self.dm.radio_FIR,SIGNAL('clicked()'),self.chose_design_methode)
        self.connect(self.dm.radio_IIR,SIGNAL('clicked()'),self.chose_design_methode)
      
    def chose_design_methode(self):
        """
        verbindung zwischen Design-Methode und Frequenz
        """
        if self.dm.radio_FIR.isChecked()==True: 
            name=self.dm.combo_FilterMethod_FIR.currentText()
        else:
            name=self.dm.combo_FilterMethod_IIR.currentText()
        print name
        if name=="Least-squares":
            self.fs.close()
            self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fpass','Fstop'],[48000,9600,12000])
            self.layout.addWidget(self.fs,3,0)
            self.fo.chekMinimal.setEnabled(False)
            self.fo.chekManual.setChecked(True)
        if name=="Equiripple":
            self.fs.close()
            self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fpass','Fstop'],[48000,9600,12000])
            self.layout.addWidget(self.fs,3,0)
            self.fo.chekMinimal.setEnabled(True)
            self.fo.chekManual.setChecked(True)
        if name=="Window":
            self.fs.close()
            self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fc'],[48000,10800])
            self.layout.addWidget(self.fs,3,0)
            self.fo.chekMinimal.setEnabled(False)
            self.fo.chekManual.setChecked(True)
        if name=="Butterworth":
            self.fs.close()
            self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fc'],[48000,10800])
            self.layout.addWidget(self.fs,3,0)
            self.fo.chekMinimal.setEnabled(True)
            self.fo.chekManual.setChecked(True)
        if name=='Elliptic':
            self.fs.close()
            self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fpass'],[48000,9600])
            self.layout.addWidget(self.fs,3,0)
            self.fo.chekMinimal.setEnabled(True)
            self.fo.chekManual.setChecked(True)
        if name=="Chebyshev":
            self.fs.close()
            self.fs=Frequency_Specification.Frequency_Specification(['Fs','Fpass'],[48000,9600])
            self.layout.addWidget(self.fs,3,0)
            self.fo.chekMinimal.setEnabled(True)
            self.fo.chekManual.setChecked(True)
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Window()
    form.show()
   
    app.exec_()


   
        



 