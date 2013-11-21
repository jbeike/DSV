# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:21:19 2013
MAINWINDOW

@author: beike
"""
import Design_Method,ResponseType,FilterOrder,Frequency_Specification,Unit_Box
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL

class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()        
        self.initUI()
        self.chose_design_list=(['Least-squares','LP',['Fs','Fpass','Fstop'],[48000,9600,12000],False,True],
                               ['Least-squares','HP',['Fs','Fstop','Fpass'],[48000,9600,12000],False,True],
                               ['Least-squares','BP',['Fs','Fstop1','Fpass1','Fstop2','Fpass2'],[48000,7200,9600,12000,14400],False,True],
                               ['Least-squares','BS',['Fs','Fpass1','Fstop1','Fpass2','Fstop2'],[48000,7200,9600,12000,14400],False,True],
                               ['Equiripple','LP',['Fs','Fpass','Fstop'],[48000,9600,12000],True,True],
                               ['Equiripple','HP',['Fs','Fstop','Fpass'],[48000,9600,12000],True,True],
                               ['Equiripple','BP',['Fs','Fstop1','Fpass1','Fstop2','Fpass2'],[48000,7200,9600,12000,14400],True,True],
                               ['Equiripple','BS',['Fs','Fpass1','Fstop1','Fpass2','Fstop2'],[48000,7200,9600,12000,14400],True,True],      
                               ['Window','LP',['Fs','Fc'],[48000,10800],False,True],
                               ['Window','HP',['Fs','Fc'],[48000,10800],False,True],
                               ['Window','BP',['Fs','Fc1','Fc2'],[48000,8400,13200],False,True],
                               ['Window','BS',['Fs','Fc1','Fc2'],[48000,8400,13200],False,True], 
                               ['Butterworth','LP',['Fs','Fc'],[48000,10800],True,True],
                               ['Butterworth','HP',['Fs','Fc'],[48000,10800],True,True],
                               ['Butterworth','BP',['Fs','Fc1','Fc2'],[48000,8400,13200],True,True],
                               ['Butterworth','BS',['Fs','Fc1','Fc2'],[48000,8400,13200],True,True],
                               ['Elliptic','LP',['Fs','Fpass'],[48000,9600],True,True],
                               ['Elliptic','HP',['Fs','Fpass'],[48000,14400],True,True],
                               ['Elliptic','BP',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True],
                               ['Elliptic','BS',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True],
                               ['Chebyshev','LP',['Fs','Fpass'],[48000,9600],True,True],
                               ['Chebyshev','HP',['Fs','Fpass'],[48000,14400],True,True],
                               ['Chebyshev','BP',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True],
                               ['Chebyshev','BS',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True],
        )
        
    def initUI(self): 
   
        self.rs=ResponseType.ResponseType()
        self.dm=Design_Method.Design_Method()
        self.fo=FilterOrder.FilterOrder()
        self.fs=Unit_Box.Unit_Box(["Hz","Normalize 0 to 1","kHz","MHz","GHz"],['Fs','Fpass','Fstop'],[48000,9600,12000])
        self.ms=Unit_Box.Unit_Box(["dB","Linear"],['Apass','Astop'],[1,80])
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
        print "-----------------------------------------"
        resp_type=self.rs.get_selected_button()
        if self.dm.radio_FIR.isChecked()==True: 
            filtname=self.dm.combo_FilterMethod_FIR.currentText()
        else:
            filtname=self.dm.combo_FilterMethod_IIR.currentText()
        print filtname + resp_type
        j=0
        i=0
        while i==0:
            print self.chose_design_list[j][0]+":"+self.chose_design_list[j][1]
            if self.chose_design_list[j][0]==filtname and self.chose_design_list[j][1]==resp_type:
                i=1
                chosen=self.chose_design_list[j][2:]
                print chosen
            j=j+1
        print "-----------------------------------------"   
        self.rebild_window(chosen[0],chosen[1],chosen[2],chosen[3])
        
    def rebild_window(self,liste=[],default=[],enMin=True,chekMan=True):
        

        self.fs.Load_txt(liste,default)

        self.fo.chekMinimal.setEnabled(enMin)
        self.fo.chekManual.setChecked(chekMan)
        
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Window()
    form.show()
   
    app.exec_()


   
        



 