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

class Txt_Box(QtGui.QWidget):
    
    def __init__(self, text,lab=[] ,default=[]):
        super(Txt_Box, self).__init__()   
        self.lab_namen=lab
        self.labels= []
        self.default_werte=default
        self.textfield=[]
        print self.default_werte
        self.txt=text
        self.initUI()
       
        
    def initUI(self): 
        anz=len(self.lab_namen)
        i=0
        
        self.layout=QtGui.QGridLayout()
        self.text=QtGui.QLabel(self)
        self.text.setText(str(self.txt))
        self.WLayout=QtGui.QVBoxLayout()
        self.WLayout.addWidget(self.text)

        while (i<anz):
           
            self.labels.append(QtGui.QLabel(self))
            self.textfield.append(QtGui.QLineEdit(str(self.default_werte[i])))
            self.labels[i].setText(self.lab_namen[i])

            self.layout.addWidget(self.labels[i],(i),0)
            self.layout.addWidget(self.textfield[i],(i),1)
            i=i+1
            
        self.WLayout.addLayout(self.layout)
        self.setLayout(self.WLayout)
        
    def Load_txt(self,text,lab=[] ,default=[])  :
        print "------------------------------------"
        print self.lab_namen
        i=0;
        print "len neu"+str(len(lab))+":"
        print lab
        print "len alt"+str(len(self.lab_namen))+":"
        self.text.setText(text)
        print self.lab_namen
        if (len(self.lab_namen)>len(lab)):
            maximal=len(self.lab_namen)
            minimal=len(lab)
        else:
            maximal=len(lab)
            minimal=len(self.lab_namen)
        print maximal    
        while (i<maximal):
            
            if (i>(len(lab)-1)):
                print 'löschen'
                self.Loesche_elm(len(lab))
            elif (i>(len(self.lab_namen)-1)):
                self.add_elm(i,lab[i],default[i])

            else:
                if (self.lab_namen[i]!=lab[i]):  
                    
                    self.labels[i].setText(lab[i])
                    self.lab_namen[i]=lab[i]
                    self.default_werte[i]=default[i]
                    self.textfield[i].setText(str(default[i]))
                    print str(i)+":"+self.labels[i].text()+":"+self.textfield[i].text()
                   # print self.labels[i+1].text() + self.textfield[i+1].text()
                else:
                    print"Namen behalten, Wert behalten"
                    print str(i)+":"+self.labels[i].text()+":"+self.textfield[i].text()
                    
            i=i+1
            
       
        print self.lab_namen
       
        self.setLayout(self.WLayout)
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
 
    
if __name__ == '__main__':
    text="asdfa"
    lab=['a','b','c',]
    default=[4,5,6]
    app = QtGui.QApplication(sys.argv)
    form=Txt_Box(text,lab,default)
    
    form.show()
    form.Load_txt("HAllo",['a','a','a','a'],[1,1,1,1])
    form.Load_txt(text,['a','s'],[1,5])
    app.exec_()