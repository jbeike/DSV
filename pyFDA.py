# -*- coding: iso-8859-15 -*-
#=========================================================================
# pyFDA.py
#
# Demonstrate different filter design methods and compare results
# to specifications
# Initial code for planned pyFDA tool
# 
# (c) 2012-Oct-30 Christian Münker
#=========================================================================
from __future__ import division
import numpy as np
from numpy import sin, cos, pi, array, arange, log10, zeros, tan, asarray
import scipy.signal as sig

#matplotlib.use('qt4agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, grid, stem, xlabel, ylabel, title

import sys
#import mayavi.mlab as mlab
import my_dsp_lib_v3 as dsp
#================================

DEF_PRINT = False    # Print plots to files?
# Path and base-name of plot-Files:
PRINT_PATH = ('D:/Daten/HM/dsvFPGA/Uebungen/HM/plots/ueb-FIL-Linphase_Amp_ML_') 
PRINT_TYPE = '.pdf' # Graphic-format
#-----------------------------------------------------------------------------
# Select plot options
#-----------------------------------------------------------------------------
SHOW_POLE_ZERO =    1     # Pole-zero-plot
SHOW_LIN_H_f =      1     # Linear plot of H(f)
SHOW_LOG_H_f =      1     # Log. plot of H(f)
SHOW_LIN_LOG_H_f =  1     # Lin./ log. plot of H(f) with specs
SHOW_PHASE =        1     # Phase response
SHOW_GRPDELAY =     1     # Group delay
SHOW_IMPZ =         1     # Impulse response

PLT_AUTOx = False # Automatic x-Axis scaling - zooming in does not work properly
PLT_DB = 'log' # 'log', 'lin' : Durchlassband log. oder lin
PLT_SB = 'log' # 'log', 'lin' : Sperrband log. oder lin
PLT_PHASE_WRAP = False # Wrap phase to +/- pi

#-----------------------------------------------------------------------------
# Frequency axis settings and Filter specs
#-----------------------------------------------------------------------------
DEF_F_RANGE = 'f_S/2' # select how to display the frequency axis:
#                       '1/2'   normalized frequency F = 0 ... 0.5 (f_S/2)
#                       '1'     normalized frequency F = 0 ... 1 (f_S)
#                       'f_S/2' absolute frequency f = 0 ... f_S/2
#                       'f_S'   absolute frequency f = 0 ... f_S
 
N_FFT = 2048 # FFT length for freqz and grpdelay
f_S = 400.0 # Samplingfrequenz 
f_S2 = f_S/2. #Samplingfrequenz 
f_DB = 40.0 #Grenzfrequenz Durchlassband
f_SB = 50.0 # Grenzfrequenz Stopband
f_sig = 12.0 # Testsignalfrequenz

FILT_TYPE = 'IIR'    # 'FIR' or 'IIR' transfer function
# Vorgabe des Ripples im DB und SB entweder linear _oder_ in dB
# hier wird del_DB und del_SB aus A_DB und A_SB bestimmt
# im GUI sollten beide Eingabemöglichkeiten vorgesehen werden
A_DB = 2 # max. Ripple im Durchlassband in dB

if FILT_TYPE == 'IIR':
    del_DB = 1 - 10**(-A_DB/20.0) 
else:
    del_DB = (10**(A_DB/20)-1) / (10**(A_DB/20)+1)

A_SB = 60 # min. Sperrdämpfung im Stoppband in dB
del_SB = 10**(-A_SB/20.0) # und linear
W_DB = 1 # default passband weight for filter calculation
W_SB = 1 # default stop band weight for filter calculation

L = 100 # manual filter order
PLT_min_dB = -A_SB-10   # Lower limit for log. Plots

#-----------------------------------------------------------------------------
# Select filter type and design method
#-----------------------------------------------------------------------------

                    
# select FIR design method: 'WIN','WIN2','REMEZ', 
# select 'MANUAL' for direct coeff. entry
FILT_FIR_METHOD = 'WIN' # 'WIN','WIN2','REMEZ', 'MANUAL'

# set FIR window type for 'WIN' and 'WIN2',
# available windows: 'boxcar', 'hann', 'bartlett', 'nuttall' ...
FILT_FIR_WINDOW = 'hann'

# set FIR coefficients for FILT_FIR_METHOD = 'MANUAL'
#FILT_FIR_COEFFS = [1, 2, 3, 4, 5]
#FILT_FIR_COEFFS = [1, 0, 1, 0, 1, 0, 1]
FILT_FIR_COEFFS = [-1/8, 0, 5/8, 1, 5/8, 0, -1/8]
FILT_FIR_COEFFS = [-0.07, 0.43, -0.43, 0.07]
FILT_FIR_COEFFS = [1,0,0,0,-1]
FILT_FIR_COEFFS = [1,0,2,0,1]

#FILT_FIR_COEFFS = 1./32 * np.ones(32)

# select IIR design method
FILT_IIR_METHOD = 'PY_DESIGN' # : Select a FILT_IIR_TYPE
#FILT_IIR_METHOD = 'MANUAL'  #: Manual coefficients entry

FILT_IIR_TYPE = 'ellip'# 'ellip' # 'cheby1',  'cheby2', 'butter' 'bessel'

# set IIR coefficients for FILT_FIR_METHOD = 'MANUAL'
FILT_IIR_COEFFS = ([1, 1],[1, -1.5, 0.9])
#FILT_IIR_COEFFS = ([1,0,0,0,-1],[-1,1])
FILT_IIR_COEFFS = (np.convolve([1,0,2,0,1], [1,1]),[1, 0,1])

###########################################################################
################ NO USER INPUTS AFTER THIS LINE ###########################
###########################################################################
#==========================================================================
# relative Grenzfrequenzen auf Abtastfrequenz bezogen
#==========================================================================
F_DB = f_DB/f_S
F_SB = f_SB/f_S
F_sig = f_sig / f_S

#==========================================================================
# Frequenzachse skalieren und Label wählen
#==========================================================================
whole = False
if DEF_F_RANGE == 'f_S/2':
    f_range = (0, f_S/2) # define tuple for x-axis
elif DEF_F_RANGE == 'f_S':
    f_range = (0, f_S)
    whole = True
elif DEF_F_RANGE == '1/2':
    f_S = 1.
    f_range = (0, 0.5)
elif DEF_F_RANGE == '1':
    f_S = 1.
    f_range = (0, 1)
    whole = True
else: sys.exit("Ungültiges Format für DEF_F_RANGE!")  
T_S = 1/f_S
#
# Define x-axis labels depending on the sampling frequency
if f_S == 1:
    my_x_axis_f = r'Norm. Frequenz $F = f / f_S \; \rightarrow$'
    my_x_axis_t = r'Sample $n$'
    f_scale = 1.; f_unit = ''; t_unit = ''; N_F = 2
else:    
    if (f_S <= 2.) and (f_S > 2.e-3):
        f_scale = 1.e3; f_unit = 'mHz'; t_unit = 's'
    if (f_S <= 2.e3) and (f_S > 2.):
        f_scale = 1.; f_unit = 'Hz'; t_unit = 'ms'
    if (f_S <= 2.e6) and (f_S > 2.e3):
        f_scale = 1.e-3; f_unit = 'kHz'; t_unit = 'us'
    if (f_S <= 2.e9) and (f_S > 2.e6):
        f_scale = 1.e-6; f_unit = 'MHz'; t_unit = 'ns'
    if (f_S <= 2.e12) and (f_S > 2.e9):
        f_scale = 1.e-6; f_unit = 'GHz'; t_unit = 'ps'
    # calculate number of fractional places for a nice display 
    N_F = str(int(3 - np.floor(log10(f_S * f_scale))))
    N_F_str = '%.' + N_F + 'f'
    if PLT_AUTOx:
        my_x_axis_f = 'Frequenz ['+ f_unit +'] ->'
        my_x_axis_t = 'Zeit ['+ t_unit + '] ->'
    else:
        my_x_axis_f = 'Frequenz [Hz] ->'
        my_x_axis_t = 'Zeit [s] ->'    
   

##############################################################################
##############################################################################
#
# FIR-Filterentwurf
#
# Ergebnis ist jeweils Spaltenvektor mit Zählerkoeffizienten
# bzw. Impulsantwort des FIR-Filters 
if FILT_TYPE == 'FIR':

    aa = 1 # Spaltenvektor der Nennerkoeffizienten = 1 bei FIR-Filtern 
    
    #=======================================================================
    ## FIRWIN: Filterentwurf mit gefensterter (Default: Hamming) 
    #          Fourier-Approximation (entspricht fir1 bei Matlab / Octave)
    # scipy.signal.firwin(numtaps, cutoff, width=None, window='hamming', 
    #                     pass_zero=True, scale=True, nyq=1.0)
    #
    if FILT_FIR_METHOD == 'WIN': 
    #
    # Hier wird die -6 dB Grenzfrequenz ( bezogen auf f_S/2 ) spezifiziert, 
    # kein Übergangsbereich wie bei firls -> ungünstig, da ein don't care - 
    # Bereich zwischen f_DB und f_SB nicht gezielt ausgenutzt werden kann! 
    # Dafür kann über die Auswahl des Fenstertyps "Finetuning" betrieben werden.
    # Mit pass_zero = True wird |H(f=0)| = 1 (Tiefpass, BP), 
    # mit pass_zero = False wird |H(f=f_S/2| = 1 (Hochpass, BS) erzwungen.
    # Für alle Filtertypen definiert der Frequenzvektor F die Eckfrequenzen
    # der Durchlassbänder. F=[0.35 0.55] und pass_zero = 1 erzeugt Bandpass
        bb = sig.firwin( L, F_DB*2.0, window=FILT_FIR_WINDOW )
 
 
    elif FILT_FIR_METHOD == 'WIN2': 
    #=======================================================================
    ## FIRWIN2: Frequency Sampling FIR-Filterentwurf: Es wird ein linearphas.
    #           Filter erzeugt, das bei den Frequenzen 'freq' die Verstärkung 
    #           'gain' hat (entsprechend fir2 bei Matlab / Octave)
    # scipy.signal.firwin2(numtaps, freq, gain, nfreqs=None, window='hamming',
    #                           nyq=1.0, antisymmetric=False)
    #
    # Mit antisymmetric = True werden Filter mit ungerader Symmetrie gewählt 
    # (Typ III oder IV), je nachdem ob numtaps gerade oder ungerade ist, wird 
    # der Typ weiter eingeschränkt.
        bb = sig.firwin2( L, [0, F_DB, F_SB, 1], [1, 1, 0, 0], 
                         window=FILT_FIR_WINDOW )
    # Example for Multi-band Hilbert Filter taken from Matlab firls reference
    #    F = [0, 0.3, 0.4, 0.6, 0.7, 0.9, 1]; A = [0, 1, 0, 0, 0.5, 0.5, 0]
    #    bb = sig.firwin2( 25, F,A, window='boxcar', antisymmetric=True )
    #
    
    elif FILT_FIR_METHOD == 'REMEZ':     
    #=======================================================================
    # Filterentwurf mit Parks-McClellan / Remez / Equiripple ... Algorithmus
    #
    # Angabe von Frequenz/Amplituden Punkten im Durchlassband und Sperrband, 
    #    optional mit Gewichtung (hier: 1 im Durchlassband, 4 im Sperrband)
#        print dsp.remlplen_kaiser(F_DB,F_SB,del_DB,del_SB)
        print dsp.remlplen_herrmann(F_DB,F_SB,del_DB,del_SB)
        print dsp.remlplen_ichige(F_DB,F_SB,del_DB,del_SB)
        L = dsp.remlplen_ichige(F_DB,F_SB,del_DB,del_SB) + 1
#        L, FF, A, W = dsp.remezord([F_DB, F_SB],[1,0],[A_DB_log, A_SB],Hz = 1, alg='kaiser' )
 #       bb = sig.remez(L, FF, A, W, Hz = 1)
        W = max(del_DB,del_SB) / asarray([del_DB, del_SB])
        # the weight of each band is chosen as the inverse of the targeted error
        #  (stricter design target => higher weight).
        #  we could normalize each entry in w to (err1+err2+err3+err4+err5)
        # but it would appear as common factor in all entries and therefore make no difference.
        #   err1 = 1 - 10 ^ (-ripple1_dB / 20);
        #   err2 = 10 ^ (-att2_dB / 20);
        #   err3 = (1 - 10 ^ (-ripple3_dB / 20)) * 0.5
#        w = [1/err1 1/err2 1/err3 1/err4 1/err5];
        print W
        bb = sig.remez(L,[0,F_DB, F_SB,0.5],[1,0], weight = W, Hz = 1)
    #
    #===================================================

    elif FILT_FIR_METHOD == 'MANUAL':
        bb = FILT_FIR_COEFFS 

else: # FILT = 'IIR'

##############################################################################
#
# IIR-Filterentwurf 
#
# Hinweise: 
#- Toleranzband im DB ist bei IIR-Entwurf definiert zwischen 0 ... -A_DB
#- Filterentwurf über [bb,aa] = ... führt zu numerischen Problemen bei Filtern
#   höherer Ordnung (ca. L > 10, selbst Ausprobieren!) Alternative Form:
#   [z,p,g] = ... liefert Nullstellen, Pole und Gain
#
#===================================================
# Butterworth-Filter
# Grenzfrequenz definiert -3dB Frequenz und muss ggf. manuell angepasst werden!
# -> ausprobieren für optimales Ergebnis oder Funktion buttord verwenden!
# Ergebnis ist Ordnung L und normierte -3dB Grenzfrequenz F_c
#L = 9 # manuelle Wahl
#[bb,aa] = butter(L, F_DB * 1.07) # manuelle Wahl
#    [L,F_c] = sig.buttord(F_DB, F_SB, A_DB, A_SB)
#    [bb,aa] = sig.butter(L, F_c) 
#===================================================
# Bessel-Filter
# Grenzfrequenz definiert -3dB Frequenz und muss ggf. manuell angepasst werden!
# -> ausprobieren für optimales Ergebnis!
#[bb,aa] = maxflat(L, F_DB * 1.07)
#===================================================
# Elliptisches Filter:
# Spezifikation sind hier maximaler Ripple im Durchlass- und Sperrband
#L = 4 # manuelle Wahl
# Funktion ellipord liefert Abschätzung für Ordnung sowie die Eckfrequenz des DB
    if FILT_IIR_METHOD == 'PY_DESIGN':       
        [bb, aa] = sig.iirdesign(F_DB*2, F_SB*2, A_DB, A_SB, 
            ftype=FILT_IIR_TYPE)
    else:
        [bb, aa] = FILT_IIR_COEFFS
##############################################################################

[w, H] = sig.freqz(bb, aa, N_FFT, whole)# calculate H(w) along the 
                                        # upper half of unity circle
                                        # w runs from 0 ... pi, length = N_FFT

f = w / (2 * pi) * f_S                  # translate w to absolute frequencies
F_DB_index = np.floor(F_DB * 2 * N_FFT) # calculate index of f_DB
F_SB_index = np.floor(F_SB * 2 * N_FFT) # calculate index of f_SB

print max(f), f_S, F_DB, F_DB_index

H_abs = abs(H)
H_max = max(H_abs); H_max_dB = 20*log10(H_max); F_max = f[np.argmax(H_abs)]
H_max_DB = max(H_abs[0:F_DB_index])
F_max_DB = f[np.argmax(H_abs[0:F_DB_index])]
H_min_DB = min(H_abs[0:F_DB_index])
F_min_DB = f[np.argmin(H_abs[0:F_DB_index])]

H_max_SB = max(H_abs[F_SB_index:len(H_abs)])
F_max_SB = f[np.argmax(H_abs[F_SB_index:len(H_abs)]) + F_SB_index]
H_min_SB = min(H_abs[F_SB_index:len(H_abs)])
F_min_SB = f[np.argmin(H_abs[F_SB_index:len(H_abs)]) + F_SB_index]
#
H_min = min(H_abs); H_min_dB = 20*log10(H_min); F_min = f[np.argmin(H_abs)]
min_dB = np.floor(max(PLT_min_dB, H_min_dB) / 10) * 10

nulls = np.roots(bb)
poles = np.roots(aa)

#################################################################
#                                                               #
#            Print Filter properties                            #
#                                                               #
#################################################################

F_test = array([F_DB, F_sig, F_SB]) # Vektor mit Testfrequenzen
Text_test = ('F_DB', 'F_sig', 'F_SB')
# Berechne Frequenzantwort bei Testfrequenzen und gebe sie aus:
[w1, H_test] = sig.freqz(bb, aa, F_test * 2.0 * pi)
f1 = w1  * f_S / (2.0 * pi)
print('       A_DB        |        A_SB ')
print('%-3.3f dB | %-3.5f | %-3.2f dB | %-3.5f\n' % (A_DB, del_DB,\
                                                   A_SB, del_SB))
#if FILT_TYPE == 'FIR':
#    print 'Ordnung: L = ', len(bb)-1
#    print 'bb = ', bb
#else:
#    print 'Ordnung: L = ', len(aa)-1 
#    print 'bb = ', bb
#    print 'aa = ', aa
        
print '============ Filter Characteristics ================\n'
print '  Test Case  |  f (Hz)    |   |H(f)|   | |H(f)| (dB)'
print '----------------------------------------------------'
for i in range(len(H_test)):
    print'{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f}'\
        .format(Text_test[i], f1[i], abs(H_test[i]), 20*log10(abs(H_test[i])))
print '{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f} '\
    .format('Maximum DB',F_max_DB, H_max_DB, 20*log10(H_max_DB))
print '{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f} '\
    .format('Minimum DB', F_min_DB, H_min_DB, 20*log10(H_min_DB))
print '{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f} '\
    .format('Maximum SB', F_max_SB, H_max_SB, 20*log10(H_max_SB))
print '{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f} '\
    .format('Minimum SB', F_min_SB, H_min_SB, 20*log10(H_min_SB))
print '{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f} '\
    .format('Maximum', F_max, H_max, H_max_dB)
print '{0:12} | {1:10.3f} | {2:10.6f} | {3:9.4f} '\
    .format('Minimum', F_min, H_min, H_min_dB)
print '\n'


#################################################################
#                                                               #
#            Plot the Results                                   #
#                                                               #
#################################################################

plt.close('all') # close all "old" figures

#=========================================
## Pol/Nullstellenplan
#=========================================
if SHOW_POLE_ZERO == True:
    plt.figure(1)
    [z, p, k] = dsp.zplane(bb, aa)
    plt.title('Pol/Nullstellenplan')
    plt.grid('on')
#    plt.text(-0.95,0.0 ,'(2)')
    plt.axis([-1.1, 1.1, -1.1, 1.1])
    plt.tight_layout() 
    if DEF_PRINT == True:
        plt.savefig((PRINT_PATH +'PZ' + PRINT_TYPE))

#=========================================
## Impulsantwort
#=========================================

if SHOW_IMPZ == True:
    plt.figure(2)
    [h, td]=dsp.impz(bb, aa, f_S)  #Impulsantwort / Koeffizienten
    [ml, sl, bl] = plt.stem(td, h) 
    plt.grid('on')
    plt.setp(ml, 'markerfacecolor', 'r', 'markersize', 8)
    plt.xlabel(my_x_axis_t)
    plt.ylabel(r'$h[n] \rightarrow $', fontsize = 20)
    plt.title(r'Impulsantwort $h[n]$')
    if PLT_AUTOx: dsp.format_ticks('x', f_scale*1000, "%.3g")
    if DEF_PRINT == True:
        plt.savefig((PRINT_PATH + 'impz' + PRINT_TYPE))

#=========================================
## Linear frequency plot
#=========================================
if SHOW_LIN_H_f == True:
    plt.figure(3)
    ax3 = plt.subplot(111)
    ax3.plot(f, H_abs); plt.grid('on')
    #plt.axis(f_range + (0., 1.2)
    plt.title(r'Betragsfrequenzgang')
    plt.xlabel(my_x_axis_f)
    plt.ylabel(r'$|H(\mathrm{e}^{\mathrm{j} 2 \pi F})|\; \rightarrow $')

    if PLT_AUTOx: dsp.format_ticks('x', f_scale, N_F_str)  
    plt.tight_layout() # pad=1.2, h_pad=None, w_pad=None
    if DEF_PRINT == True:
        plt.savefig(PRINT_PATH + 'lin' + PRINT_TYPE)
        
#=========================================
## Log frequency plot
#=========================================
if SHOW_LOG_H_f == True:
    plt.figure(4)
    plt.plot(f, 20 * log10(abs(H))); plt.grid('on')
    #plt.axis(f_range + (0., 1.2)
    plt.title(r'Log. Betragsfrequenzgang in dB')
    plt.xlabel(my_x_axis_f)
    plt.ylabel(r'$20\, \log \,|H(\mathrm{e}^{\mathrm{j} 2 \pi F})|\;\rightarrow $')
    plt.ylim(PLT_min_dB, 20*log10(H_max))
    if PLT_AUTOx: dsp.format_ticks('x', f_scale, N_F_str)
    plt.tight_layout()
    if DEF_PRINT == True:
        plt.savefig(PRINT_PATH + 'log' + PRINT_TYPE)

#=========================================
## Lin. (DB) / log. (SB) Frequenzgang mit Spezifikationen
#=========================================
if SHOW_LIN_LOG_H_f == True:
    plt.figure(5)
    plt.subplot (111); grid('on')
    if PLT_SB == 'log':
        if FILT_TYPE == 'FIR':
            A_DB_max = 20*log10(1+del_DB)
        else: # IIR log
            A_DB_max = 0
        A_DB_min = 20*log10(1-del_DB)
        A_SB_max = -A_SB

        plot(f, 20 * log10(H_abs), 'r')
        plt.axis(f_range + (PLT_min_dB, A_DB_max + 1))
        plt.ylabel('$|H(f)|$ in dB')
    else: #  SB 'lin'
        if FILT_TYPE == 'FIR':
            A_DB_max = 1 + del_DB 
        else:
            A_DB_max = 1
        A_DB_min = 1 - del_DB
        A_SB_max = del_SB
        plot(f, H_abs, 'r')
        plt.axis(f_range + (0, (A_DB_max)*1.02))
        plt.ylabel('$|H(f)|$')
        plt.tight_layout()
        
    plot([0, F_DB*f_S],[A_DB_min, A_DB_min], 'b--') # untere DB-Gr.  
    plot([0, F_SB*f_S],[A_DB_max, A_DB_max], 'b--') # obere DB-Gr.
    plot([F_DB*f_S, F_DB*f_S],[A_DB_min, A_DB_min-10],'b--')# seit. DB-Gr
    plot([F_SB*f_S, f_S],[A_SB_max, A_SB_max],'b--') # obere SB-Grenze
    plot([F_SB*f_S, F_SB*f_S],[A_DB_max, A_SB_max],'b--') # seit. SB-Grenze
    
    plt.title('Betragsfrequenzgang')
    plt.xlabel(my_x_axis_f)
    if PLT_AUTOx: dsp.format_ticks('x', f_scale, N_F_str) 
    plt.tight_layout()
    ########## Inset plot ############################
    ax1 = plt.axes([0.65, 0.61, .3, .3]); grid ('on') # x,y,dx,dy
    if PLT_DB == 'log':
        if FILT_TYPE == 'FIR': # 'DB FIR log'
            A_DB_max = 20*log10 (1+del_DB)
        else: # 'DB IIR log'
            A_DB_max = 0
        A_DB_min = 20*log10 (1-del_DB)
        A_SB_max = -A_SB

        plot(f, 20 * log10(H_abs), 'r')
        plt.axis([0, F_DB * f_S * 1.1, A_DB_min*1.1, 
                  A_DB_max-A_DB_min*0.1])
        plt.ylabel('$|H(f)|$ in dB')
    else: #  DB 'lin'
        if FILT_TYPE == 'FIR': #  'DB FIR lin'
            A_DB_max = 1 + del_DB
        else: # 'DB IIR lin'
            A_DB_max = 1
        A_DB_min = 1 - del_DB
        A_SB_max = del_SB
        plot(f, H_abs, 'r')
        plt.axis([0, F_DB * f_S * 1.1, A_DB_min - (1- A_DB_min)*0.2, 
                  A_DB_max + (1- A_DB_min)*0.2])
        plt.ylabel('$|H(f)|$')    
    plot([0, F_DB*f_S],[A_DB_min, A_DB_min], 'b--') # untere DB-Gr.  
    plot([0, F_SB*f_S],[A_DB_max, A_DB_max], 'b--') # obere DB-Gr.
    plot([F_DB*f_S, F_DB*f_S],[A_DB_min, A_DB_min-10],'b--')# seit. DB-Gr
    plot([F_SB*f_S, f_S],[A_SB_max, A_SB_max],'b--') # obere SB-Grenze
    plot([F_SB*f_S, F_SB*f_S],[A_DB_max, A_SB_max],'b--') # seit. SB-Grenze

    if DEF_PRINT == True:
        plt.savefig(PRINT_PATH +'linlog'+ PRINT_TYPE)

#=========================================
## Phasengang 
#=========================================#
if SHOW_PHASE == True:
    fig6 = plt.figure(6)
    ax6 = fig6.add_subplot(111)
    if PLT_PHASE_WRAP == True:
        ax6.plot(f, np.angle(H) / pi)
    else:
        ax6.plot(f, np.unwrap(np.angle(H))/pi)
    ax6.grid('on')
    # Ohne unwrap wird Phase auf +/- pi umgebrochen
    ax6.set_title(r'Phasengang (normiert auf Vielfache von $\pi$)')
    ax6.set_xlabel(my_x_axis_f)
    ax6.set_ylabel(r'$\phi(f) / \pi \rightarrow $')
    if PLT_AUTOx: dsp.format_ticks('x',f_scale, N_F_str)  
    plt.tight_layout() 
    if DEF_PRINT == True:
        plt.savefig(PRINT_PATH +'phase'+ PRINT_TYPE)

#=========================================
## Groupdelay
#=========================================
if SHOW_GRPDELAY == True:
    fig7 = plt.figure(7)
    ax7 = fig7.add_subplot(111)
    [tau_g, w] = dsp.grpdelay(bb,aa,N_FFT, whole, f_S)
    ax7.plot(w, tau_g); plt.grid('on')
    ax7.axis(f_range + (max(min(tau_g)-0.5,0), max(tau_g) + 0.5))
    ax7.set_title(r'Group Delay $ \tau_g$') # (r: raw string)
    ax7.set_xlabel(my_x_axis_f)
    ax7.set_ylabel(r'$ \tau_g(f)/T_S$')
    if PLT_AUTOx: dsp.format_ticks('x',f_scale, N_F_str)
    plt.tight_layout()
    if DEF_PRINT == True:
        plt.savefig(PRINT_PATH +'grpdelay' + PRINT_TYPE)

plt.show()
