# -*- coding: utf-8 -*-
"""

Edited by Christian Münker, 2013
"""
import sys
# import EITHER PyQt4 OR PySide, depending on your system
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL, SLOT  
#from PySide.QtCore import *
#from PySide.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import scipy.signal as sig

N_FFT = 2048 # FFT length for freqz
#


class all_Graphs(QtGui.QWidget):
    def __init__(self,coeffs):
        QtGui.QWidget.__init__(self)
        tab_widget = QtGui.QTabWidget()
        Betr=PlotHf()
        pltHf=PlotHf()
        pltHf.pass_param(coeffs)
        pltHf.on_draw()
        tab_widget.addTab(Betr, "DEMO")
        tab_widget.addTab(pltHf, "Betragsfrequenzgang")
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tab_widget)
        
        self.setLayout(vbox)
        
        
        
        
class PlotHf(QtGui.QWidget):

    def __init__(self):        
        parent = super(PlotHf, self).__init__() 
#    def __init__(self, parent=None):      
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Plot H(f)')
        print 'plotter_Hf.__init__()'
        self.A_SB = 60   # min. Sperrdämpfung im Stoppband in dB (= min. y-Wert des Plots)
        self.pass_param() # initialize bb, aa
        self.create_main_frame()   
        self.on_draw()

    def create_main_frame(self):
   
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        
        self.axes = self.fig.add_subplot(111)
        
        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        
        # Other GUI controls: SIGNAL definitions and connections to SLOTS
        # 
       
        self.btn_draw = QtGui.QPushButton("&Draw")
        self.connect(self.btn_draw, SIGNAL('clicked()'), self.on_draw)

        self.cb_grid = QtGui.QCheckBox("Show &Grid")
        self.cb_grid.setChecked(True)  
        self.connect(self.cb_grid, SIGNAL('stateChanged(int)'), self.on_draw)
        
        lbl_lw = QtGui.QLabel('Line width:')
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(2)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QtGui.QSlider.NoTicks)
        self.connect(self.slider, SIGNAL('valueChanged(int)'), self.on_draw)
   
        #=============================================
        # Layout with box sizers
        #=============================================
          
        hbox1 = QtGui.QHBoxLayout()            
        for w in [self.btn_draw, self.cb_grid, lbl_lw, self.slider]:
            hbox1.addWidget(w)
            hbox1.setAlignment(w, QtCore.Qt.AlignVCenter)
            
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox1)
#        vbox.addLayout(hbox2)
          
        self.setLayout(vbox)
#        self.QtGui.QMainWindow.setCentralWidget(self.main_frame)
        
    def pass_param(self, coeffs = (1,1)):
        """
        Pass and split coefficients to PlotHf
        """
        self.bb = coeffs[0]
        self.aa = coeffs[1]
       # print 'plotter_HF.pass_param.bb: ', self.bb # debug
            
    def on_draw(self):
        """ Calculates the filter and redraws the figure
        """

        [W,H] = sig.freqz(self.bb, self.aa, N_FFT) # calculate H(W) for W = 0 ... pi
        print 'on_draw.plotted!', self.bb
        F = W / (2 * np.pi)

        # clear the axes and redraw the plot
        #
        self.axes.clear()        
        self.axes.grid(self.cb_grid.isChecked())
        self.axes.axis([0, 0.5, -self.A_SB-10, 2])

        self.axes.plot(F,20*np.log10(abs(H)),
                       lw = self.slider.value())
                       
        self.axes.set_ylabel(r'$|H(\mathrm{e}^{\mathrm{j} \Omega})|\; \rightarrow $')
        self.axes.set_title(r'Betragsfrequenzgang')
        self.fig.tight_layout()
        self.canvas.draw()
    
def main():
    app = QtGui.QApplication(sys.argv)
    form = PlotHf()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
