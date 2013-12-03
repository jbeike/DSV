# -*- coding: utf-8 -*-
# -*- coding: iso-8859-15 -*-
"""
This demo demonstrates how to embed a matplotlib (mpl) plot into a PyQt4 GUI application, including:

* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
Based on Code by
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
http://eli.thegreenplace.net/files/prog_code/qt_mpl_bars.py.txt
Edited by Christian Münker, 2013
"""
import sys, scipy.io
# import EITHER PyQt4 OR PySide, depending on your system
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *  
from PySide.QtCore import *
from PySide.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import scipy.signal as sig

N_FFT = 2048 # FFT length for freqz
#
A_DB = 1    # max. Ripple im Durchlassband in dB
A_SB = 60   # min. Sperrdämpfung im Stoppband in dB

class AppForm(QMainWindow):

    def __init__(self, parent=None):
        
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo: IIR-Filter Design using PyQt with Matplotlib')

        self.create_main_frame()   
      
        self.txtbox_F_DB.setText('0.1')
        self.txtbox_F_SB.setText('0.2')

        self.on_draw()

    def on_draw(self):
        """ Recalculates the filter and redraws the figure
        """
        self.F_SB = float(unicode(self.txtbox_F_SB.text()))
        self.F_DB = float(unicode(self.txtbox_F_DB.text()))
        self.FiltType = unicode(self.combo_FiltType.currentText())
        
        [bb,aa] = sig.iirdesign(self.F_DB*2, self.F_SB*2, A_DB, A_SB, ftype=self.FiltType)
        [W,H] = sig.freqz(bb,aa,N_FFT) # calculate H(W) for W = 0 ... pi
        F = W / (2 * np.pi)

        # clear the axes and redraw the plot
        #
        self.axes.clear()        
        self.axes.grid(self.cb_grid.isChecked())
        self.axes.axis([0, 0.5, -100, 2])

        self.axes.plot(F,20*np.log10(abs(H)),
                       lw = self.slider.value())
        self.axes.set_xlabel(r'$f \; \rightarrow$')      
        self.axes.set_ylabel(r'$|H(\mathrm{e}^{\mathrm{j} \Omega})|\; \rightarrow $')
        self.axes.set_title(r'Betragsfrequenzgang')

        self.canvas.draw()
        scipy.io.savemat('my_filt.mat', mdict={'aa': aa, 'bb' : bb,
                  'F_DB' : self.F_DB,'F_SB' : self.F_SB})
    # write file that can be imported to Matlab workspace
            
    def create_main_frame(self):
        self.main_frame = QWidget()
      
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        self.axes = self.fig.add_subplot(111)
        
        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Other GUI controls: SIGNAL definitions and connections to SLOTS
        # 
        self.txtbox_F_SB = QLineEdit()
        self.txtbox_F_SB.setFixedWidth(100)
        self.connect(self.txtbox_F_SB, SIGNAL('editingFinished ()'), self.on_draw)
        lbl_F_SB = QLabel('F_SB:')

        self.txtbox_F_DB = QLineEdit()
        self.txtbox_F_DB.setFixedWidth(100)
        self.connect(self.txtbox_F_DB, SIGNAL('editingFinished ()'), self.on_draw)
        lbl_F_DB = QLabel('F_DB:')
        
        self.btn_draw = QPushButton("&Draw")
        self.connect(self.btn_draw, SIGNAL('clicked()'), self.on_draw)

        self.btn_quit = QPushButton("&Quit")
        self.connect(self.btn_quit, SIGNAL('clicked()'), self, SLOT("close()"))       
        
        self.cb_grid = QCheckBox("Show &Grid")
        self.cb_grid.setChecked(True)  
        self.connect(self.cb_grid, SIGNAL('stateChanged(int)'), self.on_draw)
        
        lbl_lw = QLabel('Line width:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(2)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.NoTicks)
        self.connect(self.slider, SIGNAL('valueChanged(int)'), self.on_draw)
   
        #=============================================
        # Layout with box sizers
        #=============================================
          
        hbox1 = QHBoxLayout()            
        for w in [ lbl_F_DB, self.txtbox_F_DB,  lbl_FiltType, 
                 self.btn_draw, self.btn_quit]:
            hbox1.addWidget(w)
            hbox1.setAlignment(w, Qt.AlignVCenter)
            
        hbox2 = QHBoxLayout()       
        for w in [ lbl_F_SB, self.txtbox_F_SB, self.cb_grid,
                    lbl_lw, self.slider]:
            hbox2.addWidget(w)
            hbox2.setAlignment(w, Qt.AlignVCenter)
            
        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
          
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
    
def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
