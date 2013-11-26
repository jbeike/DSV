# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:19:33 2013

@author: beike
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:36:39 2013

@author: beike
"""
"""
Auswahl von DesignTyp,FilterMethode 
@author: Julia Beike
Datum:14.11.2013
"""
import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import SIGNAL

class Unit_Box(QtGui.QWidget):
    
    def __init__(self, unit=[],lab=[] ,default=[]):
        super(Unit_Box, self).__init__()   
        self.lab_namen=lab
        self.labels= []
        
       
        
        self.unit=[str(i) for i in unit]
        self.default_werte=default
        self.textfield=[]
        print self.default_werte
        self.initUI()
       
        
    def initUI(self): 
        anz=len(self.lab_namen)
        i=0
        
        self.layout=QtGui.QGridLayout()
        self.lab_units=QtGui.QLabel(self)
        self.lab_units.setText("Units")
        self.combo_units=QtGui.QComboBox(self)
        self.combo_units.addItems(self.unit)
        self.layout.addWidget(self.lab_units,0,0)
        self.layout.addWidget(self.combo_units,0,1)
        while (i<anz):
           
            self.labels.append(QtGui.QLabel(self))
            self.textfield.append(QtGui.QLineEdit(str(self.default_werte[i])))
            self.labels[i].setText(self.lab_namen[i])

            self.layout.addWidget(self.labels[i],(i+1),0)
            self.layout.addWidget(self.textfield[i],(i+1),1)
            i=i+1
 
 
        self.setLayout(self.layout)
        
    def Load_txt(self,lab=[] ,default=[])  :
 
        i=0;
       
        if (len(self.lab_namen)>len(lab)):
            maximal=len(self.lab_namen)
            minimal=len(lab)
        else:
            maximal=len(lab)
            minimal=len(self.lab_namen)
        print maximal    
        while (i<maximal):
            
            if (i>(len(lab)-1)):
             
                self.Loesche_elm(len(lab))
            elif (i>(len(self.lab_namen)-1)):
                self.add_elm(i,lab[i],default[i])

            else:
                if (self.lab_namen[i]!=lab[i]):  
                    
                    self.labels[i].setText(lab[i])
                    self.lab_namen[i]=lab[i]
                    self.default_werte[i]=default[i]
                    self.textfield[i].setText(str(default[i]))
      
                   # print self.labels[i+1].text() + self.textfield[i+1].text()
            i=i+1
            
       
        print self.lab_namen

        self.setLayout(self.layout)
        print "------------------------------------" 
        
    def Loesche_elm(self,i):
        
        self.layout.removeWidget(self.labels[i])
        self.layout.removeWidget(self.textfield[i])
        self.labels[i].deleteLater()
        del self.lab_namen[i]
        del self.default_werte[i]
        del self.labels[i]
        self.textfield[i].deleteLater()
        del self.textfield[i]  
        
    def add_elm(self,i,lab_name,defaultw)  :
       self.labels.append(QtGui.QLabel(self))
       self.lab_namen.append(lab_name)
       self.default_werte.append(defaultw)
       self.textfield.append(QtGui.QLineEdit(str (defaultw)))
       self.labels[i].setText(lab_name)
       print str(i)+":"+self.labels[i].text()+":"+self.textfield[i].text()
       self.layout.addWidget(self.labels[i],(i+1),0)
       self.layout.addWidget(self.textfield[i],(i+1),1)
      
    def get_elm(self):
        
        self.werte=len(self.textfield)*[1]
        i=0
        print "---"
        print len(self.lab_namen)
        while(i<len(self.textfield)):
            self.werte[i]=self.textfield[i].text()
            print self.werte[i]
        return (self.combo_units.currentText(),self.lab_namen,self.werte) 
         
 
    
if __name__ == '__main__':
    unit=['bf','bf','bf',]
    lab=['a','b','c',]
    default=[4,5,6]
    app = QtGui.QApplication(sys.argv)
    form=Unit_Box(unit,lab,default)
    form.Load_txt(['a','b','c','d'],[1,2,3,10])
    form.Load_txt(['d','b','a'],[1,2,3])
    i=form.get_elm()
    print i
    form.show()
   
    app.exec_()
