# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:21:19 2013
MAINWINDOW

@author: beike
"""
import Design_Method,ResponseType,FilterOrder,Unit_Box,Txt_Box
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
"""
Zur Eingabe aller Parameter und Einstellungen
"""
class Chose_Param(QtGui.QWidget):
    
    def __init__(self):
        super(Chose_Param, self).__init__()        
        self.initUI()
        #Alle "Eigenschaften" der verschiedenen Filtertypen
        self.chose_design_list=(
                               ['Least-squares','LP',['Fs','Fpass','Fstop'],[48000,9600,12000],False,True,"tb",["Enter a weight value for each band below",["Wpass","Wstop"],[1,1]]],
                               ['Least-squares','HP',['Fs','Fstop','Fpass'],[48000,9600,12000],False,True,"tb",["Enter a weight value for each band below",["Wstop","Wpass"],[1,1]]],
                               ['Least-squares','BP',['Fs','Fstop1','Fpass1','Fstop2','Fpass2'],[48000,7200,9600,12000,14400],False,True,"tb",["Enter a weight value for each band below",["Wstop1","Wpass","Wstop2"],[1,1,1]]],
                               ['Least-squares','BS',['Fs','Fpass1','Fstop1','Fpass2','Fstop2'],[48000,7200,9600,12000,14400],False,True,"tb",["Enter a weight value for each band below",["Wpass1","Wstop","Wpass2"],[1,1,1]]],
                               ['Equiripple','LP',['Fs','Fpass','Fstop'],[48000,9600,12000],True,True,"tb",["Enter a weight value for each band below",["Wpass","Wstop"],[1,1]]],
                               ['Equiripple','HP',['Fs','Fstop','Fpass'],[48000,9600,12000],True,True,False,True,"tb",["Enter a weight value for each band below",["Wstop","Wpass"],[1,1]]],
                               ['Equiripple','BP',['Fs','Fstop1','Fpass1','Fstop2','Fpass2'],[48000,7200,9600,12000,14400],True,True,"tb",["Enter a weight value for each band below",["Wstop1","Wpass","Wstop2"],[1,1,1]]],
                               ['Equiripple','BS',['Fs','Fpass1','Fstop1','Fpass2','Fstop2'],[48000,7200,9600,12000,14400],True,True,"tb",["Enter a weight value for each band below",["Wpass1","Wstop","Wpass2"],[1,1,1]]],      
                               ['Window','LP',['Fs','Fc'],[48000,10800],False,True,"txt","The attenuation at cutoff frequencies is fixed at 6 dB (half the passband gain)"],
                               ['Window','HP',['Fs','Fc'],[48000,10800],False,True,"txt","The attenuation at cutoff frequencies is fixed at 6 dB (half the passband gain)"],
                               ['Window','BP',['Fs','Fc1','Fc2'],[48000,8400,13200],False,True,"txt","The attenuation at cutoff frequencies is fixed at 6 dB (half the passband gain)"],
                               ['Window','BS',['Fs','Fc1','Fc2'],[48000,8400,13200],False,True,"txt","The attenuation at cutoff frequencies is fixed at 6 dB (half the passband gain)"], 
                               ['Butterworth','LP',['Fs','Fc'],[48000,10800],True,True,"txt","The attenuation at cutoff frequencies is fixed at 3 dB (half the passband power)"],
                               ['Butterworth','HP',['Fs','Fc'],[48000,10800],True,True,"txt","The attenuation at cutoff frequencies is fixed at 3 dB (half the passband power)"],
                               ['Butterworth','BP',['Fs','Fc1','Fc2'],[48000,8400,13200],True,True,"txt","The attenuation at cutoff frequencies is fixed at 3 dB (half the passband power)"],
                               ['Butterworth','BS',['Fs','Fc1','Fc2'],[48000,8400,13200],True,True,"txt","The attenuation at cutoff frequencies is fixed at 3 dB (half the passband power)"],
                               ['Elliptic','LP',['Fs','Fpass'],[48000,9600],True,True,"ub",[["DB","Squared"],["Apass","Astop"],[1,80]]],
                               ['Elliptic','HP',['Fs','Fpass'],[48000,14400],True,True,"ub",[["DB","Squared"],["Astop","Apass"],[80,1]]],
                               ['Elliptic','BP',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True,"ub",[["DB","Squared"],["Astopp1","Apass","Astop2"],[60,1,80]]],
                               ['Elliptic','BS',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True,"ub",[["DB","Squared"],["Apass1","Astop","Apass2"],[5,60,1]]],
                               ['Chebychev 1','LP',['Fs','Fpass'],[48000,9600],True,True,"ub",[["DB","Squared"],["Apass","Astop"],[1,80]]],
                               ['Chebychev 1','HP',['Fs','Fpass'],[48000,14400],True,True,"ub",[["DB","Squared"],["Astop","Apass"],[80,1]]],
                               ['Chebychev 1','BP',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True,"ub",[["DB","Squared"],["Astopp1","Apass","Astop2"],[60,1,80]]],
                               ['Chebychev 1','BS',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True,"ub",[["DB","Squared"],["Apass1","Astop","Apass2"],[5,60,1]]],
                               ['Chebychev 2','LP',['Fs','Fpass'],[48000,9600],True,True,"ub",[["DB","Squared"],["Apass","Astop"],[1,80]]],
                               ['Chebychev 2','HP',['Fs','Fpass'],[48000,14400],True,True,"ub",[["DB","Squared"],["Astop","Apass"],[80,1]]],
                               ['Chebychev 2','BP',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True,"ub",[["DB","Squared"],["Astopp1","Apass","Astop2"],[60,1,80]]],
                               ['Chebychev 2','BS',['Fs','Fpass1','Fpass2'],[48000,9600,12000],True,True,"ub",[["DB","Squared"],["Apass1","Astop","Apass2"],[5,60,1]]]
                                )                                               
        
        
    def initUI(self): 
        """
        Anlegen aller Widgets 
        fs:= Frequency Specifications 
        ms:= Magnitude Specifications (wobei es hier verschiedene Typen gibt: tb:= text+Auswahlfelder; ub:= Einheit+ Auswahlfelder; txt:= nur Text)""" 
        self.rs=ResponseType.ResponseType() 
        self.dm=Design_Method.Design_Method()
        self.fo=FilterOrder.FilterOrder()
        self.fs=Unit_Box.Unit_Box(["Hz","Normalize 0 to 1","kHz","MHz","GHz"],['Fs','Fpass','Fstop'],[48000,9600,12000])
        
        self.ms_tex=QtGui.QLabel(self)
        self.ms_tex.setText("Enter a weight value for each band below")
        self.ms_ub=Unit_Box.Unit_Box(["DB","Squared"],["Apass","Astop"],[1,80])
        self.ms_tb=Txt_Box.Txt_Box("Enter a weight value for each band below",["Wpass","Wstop"],[1,1])
        self.ms_last="tb"
        # alle Magnitude Widgets die nicht benötigt werden sind unsichtbar, aber trotzdem immer da!!
        self.ms_tex.setVisible(False)
        self.ms_ub.setVisible(False)
        self.ms_tb.setVisible(True)
        """
        LAYOUT      
        """
        
        self.layout=QtGui.QGridLayout()
        self.layout.addWidget(self.rs,0,0)
        self.layout.addWidget(self.dm,1,0)
        self.layout.addWidget(self.fo,2,0)
        self.layout.addWidget(self.fs,3,0)
        self.layout.addWidget(self.ms_tex,4,0)
        self.layout.addWidget(self.ms_tb,5,0)
        self.layout.addWidget(self.ms_ub,6,0)
        self.setLayout(self.layout)
        """
        SIGNAL
        """
         #wenn sich die Filtermethode oder der Filtertyp ändert wird chose_design_methode aufgerufen
        self.connect(self.dm.combo_FilterMethod_FIR,SIGNAL('activated(QString)'),self.chose_design_methode)
        self.connect(self.dm.combo_FilterMethod_IIR,SIGNAL('activated(QString)'),self.chose_design_methode)
        self.connect(self.dm.radio_FIR,SIGNAL('clicked()'),self.chose_design_methode)
        self.connect(self.dm.radio_IIR,SIGNAL('clicked()'),self.chose_design_methode)
        self.connect(self.rs.radio_BP,SIGNAL('clicked()'),self.chose_design_methode)
        self.connect(self.rs.radio_HP,SIGNAL('clicked()'),self.chose_design_methode)
        self.connect(self.rs.radio_LP,SIGNAL('clicked()'),self.chose_design_methode)
        self.connect(self.rs.radio_BS,SIGNAL('clicked()'),self.chose_design_methode)
    def chose_design_methode(self):
        """
        je nach Filtermethode und Frequenz werden die Werte der Widgets do,ds  neu gesetzt bzw bei ms auch noch die Sichtbarkeit verändert
        """
        #print "-----------------------------------------"
        resp_type=self.rs.get()
        if self.dm.radio_FIR.isChecked()==True: 
            filtname=self.dm.combo_FilterMethod_FIR.currentText()
        else:
            filtname=self.dm.combo_FilterMethod_IIR.currentText()
        #print filtname + resp_type
        j=i=0
        while i==0:
           # print self.chose_design_list[j][0]+":"+self.chose_design_list[j][1]
            if self.chose_design_list[j][0]==filtname and self.chose_design_list[j][1]==resp_type:
                i=1
                chosen=self.chose_design_list[j][2:]
                #print chosen
            j=j+1
        #print "-----------------------------------------"   
        self.rebild_frequ_filtOrd(chosen[0],chosen[1],chosen[2],chosen[3])
        self.rebild_mag(chosen[4],chosen[5])
        self.setLayout(self.layout)
        
        
    def rebild_frequ_filtOrd(self,liste=[],default=[],enMin=True,chekMan=True):
        """
        Hilfsfunktion zur aktualisierung des Frequenz-Widget und der FilterOrdnung
        """

        self.fs.Load_txt(liste,default)
        self.fo.chekMinimal.setEnabled(enMin)
        self.fo.chekManual.setChecked(chekMan)
        
    def rebild_mag(self,string,liste=[]):
        """
        Hilfsfunktion zur aktualisierung der MAgnitude Specifications
        """
        #print "_________________________"
       # print liste
       # print string
       # print"_________________________"
        if string=="txt":
            self.ms_tex.setText(liste)
            self.ms_tex.setVisible(True)
            self.ms_ub.setVisible(False)
            self.ms_tb.setVisible(False)
            self.ms_last="txt"
        if string=="ub" :
            self.ms_ub.Load_txt(liste[1],liste[2])
            self.ms_ub.setVisible(True)
            self.ms_tb.setVisible(False)
            self.ms_tex.setVisible(False)
            self.ms_last="ub"
        if string=="tb" :
            self.ms_tb.Load_txt(liste[0],liste[1],liste[2])
            self.ms_tb.setVisible(True)
            self.ms_tex.setVisible(False)
            self.ms_ub.setVisible(False)
            self.ms_last="tb"
            
    def get(self):
        """
        Gibt die aktuell ausgewählten Parameter zurrück
        """
        
        ret=[]
        ret.append(self.rs.get())
        ret.append(self.dm.get())
        ret.append(self.fo.get())
        ret.append(self.fs.get())
         

        if self.ms_last=="ub":
            ret.append( self.ms_ub.get())
        if self.ms_last=="tb" :
            ret.append( self.ms_tb.get())
    
        return ret  
        
        

        
        
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Chose_Param()
    form.show()
   
    app.exec_()


   
        



 