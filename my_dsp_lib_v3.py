# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 10:29:42 2012

@author: Muenker_2
"""
#
# Copyright (c) 2011 Christopher Felton, Christian Münker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# The following is derived from the slides presented by
# Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
# CSLU / OHSU, Spring Term 2011.
from __future__ import division
import string # needed for remezord?
import numpy as np
from numpy import pi, asarray, absolute, sqrt, log10, arctan,\
   ceil, hstack, mod    

import scipy.signal as signal
from scipy import special # needed for remezord
import matplotlib.pyplot as plt
from  matplotlib import patches
#from matplotlib.figure import Figure
#from matplotlib import rcParams

def H_mag(zaehler, nenner, z, lim):
    """ Calculate magnitude of H(z) or H(s) in polynomial form at the complex 
    coordinate z = x, 1j * y (skalar or array)
    The result is clipped at lim."""
#    limvec = lim * np.ones(len(z))
    try: len(zaehler)
    except TypeError:
        z_val = abs(zaehler) # zaehler is a scalar
    else:
        z_val = abs(np.polyval(zaehler,z))
    try: len(nenner)
    except TypeError:
        n_val = nenner # nenner is a scalar
    else:
        n_val = abs(np.polyval(nenner,z))
        
    return np.minimum((z_val/n_val),lim)

#----------------------------------------------------------------------
def fixed(q_obj,y):    
    """
    Implement binary quantization of signed scalar or array-like objects 
    in the form yq = IW.FW where IW and FW are the number of integer resp. 
    fractional bits; total wordlength is W = IW + FW + 1 due to the sign bit.
    
    [yq, N_over] = fixed(q_obj, y)
    
      y      is the value or vector to be quantized (matrix not yet implemented)
      q_obj  is the quantizer object, specifying the quantization operation:
    
    Parameters
    ----------
    q_obj : tuple with 2 ... 4 elements defining quantization operation;
            q_obj = (IW, FW, [[QMethod, [OMethod]])
      q_obj[0]: IW; integer word length
      q_obj[1]: FW; fractional word length; IW + FW + 1 = W (1 sign bit)
      q_obj[2]: Quantization method, optional
      - 'floor': (default) largest integer i such that i <= x (= binary truncation)
      - 'round': (binary) rounding
      - 'fix': round to nearest integer towards zero ('Betragsschneiden')
      - 'ceil': smallest integer i, such that i >= x
      - 'rint': round towards nearest int 
      - 'none': no quantization (for test purposes)
      q_obj[3]: Overflow method, optional; default = 'none'
    
    y : scalar or array-like object
    
    Returns
    -------
    yq : ndarray
    The quantized input value(s)
    N_over : integer
    Number of overflows that has occured during quantization
    
    Notes
    -----
    fixed() replaces Matlab quantizer object / function, 
    e.g. q_dsp = quantizer('fixed', 'round', [16 15], 'wrap');
    see (Matlab) help round and help quantizer/round
    16 Binärstellen insgesamt, davon 15 Fractional-Bits -> [-1.0 ... 0.9999]
    
    
    Example:
    --------
    >>> a = np.arange(0,5,0.05)
    >>> q_obj = (1,2,'round','wrap')
    >>> aq, N_over = fixed(q_obj, a)
    >>> plt.plot(a,aq)
    >>> print N_over # print number of overflows
    """

    LSB  = 2. ** (-q_obj[1])
    MSB  = 2. ** q_obj[0]
    if len(q_obj)  > 2:
        requant = q_obj[2]
    else: requant = 'floor'
    if len(q_obj) > 3:
        overflow = q_obj[3]
    else: overflow = 'none'
            
    try:
        len_y = len(y)
    except TypeError:
        # scalar:        
        yOVER_p = yOVER_n = yq = 0
#        len_y = 1
    else:
        # array:
#        LSB = np.ones(len(y)) * LSB
        yOVER_p = yOVER_n = yq = np.zeros(len(y))
        y = np.asarray(y)
    
    if   requant == 'floor':  yq = LSB * np.floor(y / LSB)
         # largest integer i, such that i <= x (= binary truncation)
    elif requant == 'round':  yq = LSB * np.round(y / LSB)
         # rounding, also = binary rounding
    elif requant == 'fix':    yq = LSB * np.fix(y / LSB)
         # round to nearest integer towards zero ("Betragsschneiden")
    elif requant == 'ceil':   yq = LSB * np.ceil(y / LSB)
         # smallest integer i, such that i >= x
    elif requant == 'rint':   yq = LSB * np.rint(y / LSB)
         # round towards nearest int 
    elif requant == 'none':   yq = y
    else: raise Exception('Unknown Requantization type %s!'%(requant))
    
    if   overflow == 'none': N_over = 0
    else: 
        yOVER_n = (yq < -MSB)  # Bool. vector with '1' for every neg. overflow
        yOVER_p = (yq >= MSB)  # Bool. vector with '1' for every pos. overflow
        N_over = np.sum(yOVER_n) + np.sum(yOVER_p) # No. of overflows
        if overflow == 'sat': # Replace overflows with +/- MSB (saturation)
            yq = yq * (~yOVER_p) * (~yOVER_n) + yOVER_p * MSB - yOVER_n * MSB
        elif overflow == 'wrap':
            yq = yq - 2. * MSB*np.fix((np.sign(yq)* MSB+ yq)/(2*MSB))
        else: raise Exception('Unknown overflow type %s!'%(overflow))
    return yq, N_over

#----------------------------------------------------------------------
def FIX_filt_MA(x, bq, aq, gq, q_mul, q_acc, verbose = True):
    """
    [s,yq] = Kap4_filt_MA(x,aq,bq,gq, q_mul, q_acc)
	FIR-Filter mit verschiedenen internen Quantisierungen: 
	q_mul beschreibt Requantisierung nach Koeffizientenmultiplikation
	q_acc beschreibt Requantisierung bei jeder Summation im Akkumulator 
	(bzw. gemeinsamen Summenpunkt)
    """
	
# Initialize vectors (also speeds up calculation)
#    Nx = len(x)
#    s = zeros(Nx) # not needed in this filter
    yq = accu_q = np.zeros(len(x))
#    bq_len = len(bq)
    x_bq = np.zeros(len(bq))
	
# Calculate filter response via difference equation with quantization:
	
    for k in range(len(x) - len(bq)):
        # weighted state-vector x at time k:
        x_bq, N_over_m = fixed(q_mul, x[k:k + len(bq)] * bq)
        # sum up x_bq to get accu[k]
        accu_q[k], N_over_a = fixed(q_acc, sum(x_bq))
    yq = accu_q * gq # scaling at the output of the accumulator
    s = x # copy state-vector
    if (N_over_m and verbose): print('Overflows in Multiplier:  ', N_over_m)
    if (N_over_a and verbose): print('Overflows in Accumulator: ', N_over_a)
         
    return yq, s
    
# nested loop would be much slower!
#  for k in range(Nx - len(bq)):
#	for i in len(bq):
#	  accu_q[k] = fixed(q_acc, (accu_q[k] + fixed(q_mul, x[k+i]*bq[i+1])))
	
    
#----------------------------------------------
# from scipy.signal.signaltools.py:
def cmplx_sort(p):
    "sort roots based on magnitude."
    p = np.asarray(p)
    if np.iscomplexobj(p):
#        indx = np.argsort(abs(p)) # so steht's bei scipy
        indx = np.argsort(p.imag) # CM, funktioniert für 
        # für meine Fälle besser, aber auch nicht immer
        # mögliche Lösung: erst nach imag, dann nach real
        # sortieren?
    else:
        indx = np.argsort(p)
    return np.take(p, indx, 0), indx
    
# from scipy.signal.signaltools.py:    
def unique_roots(p, tol=1e-3, rtype='min'):
    """
Determine unique roots and their multiplicities from a list of roots.

Parameters
----------
p : array_like
The list of roots.
tol : float, optional
The tolerance for two roots to be considered equal. Default is 1e-3.
rtype : {'max', 'min, 'avg'}, optional
How to determine the returned root if multiple roots are within
`tol` of each other.

- 'max': pick the maximum of those roots.
- 'min': pick the minimum of those roots.
- 'avg': take the average of those roots.

Returns
-------
pout : ndarray
The list of unique roots, sorted from low to high.
mult : ndarray
The multiplicity of each root.

Notes
-----
This utility function is not specific to roots but can be used for any
sequence of values for which uniqueness and multiplicity has to be
determined. For a more general routine, see `numpy.unique`.

Examples
--------
>>> vals = [0, 1.3, 1.31, 2.8, 1.25, 2.2, 10.3]
>>> uniq, mult = sp.signal.unique_roots(vals, tol=2e-2, rtype='avg')

Check which roots have multiplicity larger than 1:

>>> uniq[mult > 1]
array([ 1.305])

"""
    if rtype in ['max', 'maximum']:
        comproot = np.maximum
    elif rtype in ['min', 'minimum']:
        comproot = np.minimum
    elif rtype in ['avg', 'mean']:
        comproot = np.mean
#    p = np.atleast_1d(p).tolist() # convert scalars and arrays to list
    p_mul = [] # initialize list for multiplicities
    p_out = [] # initialize list for 
    tol = abs(tol)

    for i in range(len(p)): # p[i] is current root under test
        if ~np.isnan(p[i]): # has current root been "deleted" yet?
            p_mul.append(1)     # multiplicity of current root is at least 1
            sameroots = [p[i]]  # initialize "sameroots" list with current root
            for j in range(len(p)-i-1): # compare p[i] with rest of the roots:
                if ~np.isnan(p[i+j+1]): # has root[i+j+1] been "deleted" yet?
                    if (abs(p[i+j+1].real - p[i].real)      # dist. is less
                    + abs(p[i+j+1].imag - p[i].imag))< tol: # than tol
                        p_mul[-1] +=1   # increase multiplicity of p[i] by 1
                        sameroots.append(p[i+j+1]) # append p[i+j+1] to sa
                        p[i+j+1] = np.nan    # p[i+j+1] has been processed, delete it
            p_out.append(comproot(sameroots)) # avg/mean/max of mult. root

    return np.array(p_out), np.array(p_mul)



def zplane(b,a=1,pn_eps=1.e-2, zpk=False, style='square'):
    """Plot the poles and zeros in the complex z-plane either from the 
    coefficients (b,a) of a discrete transfer function (zpk = False) 
    or directly from the zeros and poles (z,p; zpk = True).
    """
    # TODO:
    # - polar option
    # - add keywords for size, color etc. of markers and circle -> **kwargs
    # - add option for multi-dimensional arrays and zpk data

    # Alternative: 
    # get a figure/plot
    # [z,p,k] = scipy.signal.tf2zpk -> poles and zeros 
    # Plotten über
    # scatter(real(p),imag(p))
    # scatter(real(z),imag(z))
    ax = plt.subplot(111)

    # create the unit circle
    uc = patches.Circle((0,0), radius=1, fill=False,
                        color='grey', ls='solid')
    ax.add_patch(uc)

    # Is input data given as zeros & poles (zpk = True) or 
    # as numerator & denominator coefficients (b, a) of discrete time system?
    
    if zpk == False:        
        # The coefficients are less than 1, normalize the coeficients
        if np.max(b) > 1:
            kn = np.max(b)
            b = np.array(b)/float(kn) # make sure that b is an array
        else:
            kn = 1.
    
        if np.max(a) > 1:
            kd = np.max(a)
            a = np.array(a)/float(kd) # make sure that a is an array
        else:
            kd = 1.
            
        # Calculate the poles, zeros and scaling factor
        p = np.roots(a)
        z = np.roots(b)
        k = kn/kd
    else:
        z = b; p = a; k = 1.
    # find multiple poles and zeros and their multiplicities
#    print p, z
    if len(p) < 1:
        p = np.array(0,ndmin=1) # only zeros, create equal number of poles at z = 0
        num_p = np.array(len(z),ndmin=1)
    else:   
        p, num_p = unique_roots(p, tol = pn_eps, rtype='avg')
    if len(z) > 0:
        z, num_z = unique_roots(z, tol = pn_eps, rtype='avg')
    else: 
        num_z = []
        
#    print p,z
    
    # Plot the zeros and set marker properties    
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)
    plt.setp( t1, markersize=10.0, markeredgewidth=2.0,
              markeredgecolor='b', markerfacecolor='none')

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
    plt.setp( t2, markersize=12.0, markeredgewidth=3.0,
              markeredgecolor='r', markerfacecolor='none')
              
    for i in range(len(z)):
        print 'z', i, z[i], num_z[i]
        if num_z[i] > 1:
            plt.text(np.real(z[i]), np.imag(z[i]),' (' + str(num_z[i]) +')')
            
    for i in range(len(p)):
        print 'p', i, p[i], num_p[i]
        if num_p[i] > 1:
            plt.text(np.real(p[i]), np.imag(p[i]), ' (' + str(num_p[i]) +')')

#    ax.spines['left'].set_position('center')
#    ax.spines['bottom'].set_position('center')
#    ax.spines['right'].set_visible(True)
#    ax.spines['top'].set_visible(True)

    # set the ticks
    r = 1.1
    #r = 1.1 * max(np.max(np.max(np.abs(z)),np.max(np.abs(p))),1.)
    # 
    plt.axis('equal'); plt.axis([-r, r, -r, r], aspect='equal')
    #ticks = [-1, -.5, .5, 1]; 
   # plt.xticks(ticks); #plt.yticks(ticks)


    #z=z

    return z, p, k
#-------------------------------------------------------- 
   
def mfreqz(b,a=1):
    """ Calculate and plot frequency and phase response
    from filter coefficients."""
    w,h = signal.freqz(b,a)
    h_dB = 20 * np.log10 (abs(h))
    plt.subplot(211)
    plt.plot(w/max(w),h_dB)
    plt.ylim(-150, 5)
    plt.ylabel('Magnitude (db)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Frequency response')
    plt.grid('on')
    plt.subplot(212)
    h_Phase = np.unwrap(np.arctan2(np.imag(h),np.real(h)))
    plt.plot(w/max(w),h_Phase)
    plt.ylabel('Phase (radians)')
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    plt.title(r'Phase response')
    plt.subplots_adjust(hspace=0.5)
    plt.grid('on')
#    show()
#==================================================================
#
#==================================================================
def impz(b, a=1, FS=1, N=1):
    """
Calculate impulse response of a discrete time filter, specified by 
numerator coefficients b and denominator coefficients a of the system
function H(z). 

When only b is given, the impulse response of the transversal (FIR)
filter specified by b is calculated.

Parameters
----------
b :  array_like
     Numerator coefficients (transversal part of filter)

a :  array_like (optional, default = 1 for FIR-filter)
     Denominator coefficients (recursive part of filter)
    
FS : float (optional, default: FS = 1)
     Sampling frequency. 
    
N :  float (optional)
     Number of calculated points. 
     Default: N = len(b) for FIR filters, N = 100 for IIR filters

Returns
-------
hn : ndarray with length N (see above)
td : ndarray containing the time steps with same 

    
Examples
--------
>>> b = [1,2,3] # Coefficients of H(z) = 1 + 2 z^2 + 3 z^3
>>> h, n = dsp_lib.impz(b)
"""
    try: len(a) #len_a = len(a)
    except TypeError:
         # a has len = 1 -> FIR-Filter
        impulse = np.repeat(0.,len(b)) # create float array filled with 0.
        try: len(b)
        except TypeError:
            print 'No proper filter coefficients: len(a) = len(b) = 1 !'    
    else:
        try: len(b)
        except TypeError: b = [b,] # convert scalar to array with len = 1
        impulse = np.repeat(0.,100)  # IIR-Filter
    if N > 1:
        impulse = np.repeat(0.,N)
    impulse[0] =1.0 # create dirac impulse
    hn = np.array(signal.lfilter(b,a,impulse)) # calculate impulse response
    td = np.arange(len(hn)) / FS
    
    #step = np.cumsum(hn) 
    return hn, td

#==================================================================
def grpdelay(b, a=1, nfft=512, whole='none', Fs=2.*pi):
#==================================================================    
    """
Calculate group delay of a discrete time filter, specified by 
numerator coefficients b and denominator coefficients a of the system
function H(z). 

When only b is given, the group delay of the transversal (FIR)
filter specified by b is calculated.

Parameters
----------
b :  array_like
     Numerator coefficients (transversal part of filter)

a :  array_like (optional, default = 1 for FIR-filter)
     Denominator coefficients (recursive part of filter)
     
whole : string (optional, default : 'none')
     Only when whole = 'whole' calculate group delay around 
     the complete unity circle (0 ... 2 pi)

N :  integer (optional, default: 512)
     Number of FFT-points

FS : float (optional, default: FS = 2*pi)
     Sampling frequency. 

Returns
-------
tau_g : ndarray with group delay 

w : ndarray containing the frequency points in rad (default)

    
Examples
--------
>>> b = [1,2,3] # Coefficients of H(z) = 1 + 2 z^2 + 3 z^3
>>> tau_g, td = dsp_lib.grpdelay(b)
"""
    if whole !='whole':
        nfft = 2*nfft
#
    w = Fs * np.arange(0, nfft)/nfft
    
    try: len(a)
    except TypeError: 
        a = 1; oa = 0
        c = b
        try: len(b)
        except TypeError: print 'No proper filter coefficients: len(a) = len(b) = 1 !'
    else:    
        oa = len(a)-1;             # order of a(z)
        c = np.convolve(b,a[::-1]) # c(z) = b(z)*a(1/z)*z^(-oa); a[::-1] reverses a
    try: len(b)
    except TypeError: b=1; ob=0; 
    else:    
        ob = len(b)-1;             # order of b(z)  

    oc = oa + ob;                  # order of c(z)
     
    cr = c * np.arange(0,oc+1) # multiply with ramp -> derivative of c wrt 1/z

    num = np.fft.fft(cr,nfft)
    den = np.fft.fft(c,nfft)
#
    minmag = 10 * np.spacing(1) # equivalent to matlab "eps"
    polebins = np.where(abs(den)<minmag)[0]  # find zeros, convert tuple to array
    if np.size(polebins) > 0:  # check whether polebins array is empty
        print '*** grpdelay warning: group delay singular -> setting to 0 at:'
        for i in polebins:
            print 'f = {0} '.format((Fs*i/nfft))
            num[i] = 0;
            den[i] = 1;          

    tau_g = np.real(num / den) - oa;
#    
    if whole !='whole':
        nfft = nfft/2
        tau_g = tau_g[0:nfft]
        w = w[0:nfft]

    return tau_g, w

#==================================================================
def format_ticks(xy, scale, format="%.1f"):
#==================================================================    
    """
Reformat numbers at x or y - axis. The scale can be changed to display
e.g. MHz instead of Hz. The number format can be changed as well.

Parameters
----------
xy : string, either 'x', 'y' or 'xy'
     select corresponding axis (axes) for reformatting

scale :  real,
     
format : string, 
         define C-style number formats

Returns
-------
nothing

    
Examples
--------
>>> format_ticks('x',1000.)
Scales all numbers of x-Axis by 1000, e.g. for displaying ms instead of s.
>>> format_ticks('xy',1., format = "%.2f")
Two decimal places for numbers on x- and y-axis
"""
    if xy == 'x' or xy == 'xy':
        locx,labelx = plt.xticks() # get location and content of xticks
        plt.xticks(locx, map(lambda x: format % x, locx*scale))
    if xy == 'y' or xy == 'xy':
        locy,labely = plt.yticks() # get location and content of xticks
        plt.yticks(locy, map(lambda y: format % y, locy*scale))
        
#========================================================
"""Supplies remezord method according to Scipy Ticket #475
http://projects.scipy.org/scipy/ticket/475
https://github.com/thorstenkranz/eegpy/blob/master/eegpy/filter/remezord.py
"""

#from numpy import mintypecode

 
abs = absolute
 
def findfreqs(num, den, N):
    m = np.arange(0,N)
    h = win*special.sinc(cutoff*(m-alpha))
    return h / np.sum(h,axis=0)

def oddround(x):
    """Return the nearest odd integer from x."""

    return x-mod(x,2)+1

def oddceil(x):
    """Return the smallest odd integer not less than x."""

    return oddround(x+1)
    
def remlplen_herrmann(fp,fs,dp,ds):
    """
Determine the length of the low pass filter with passband frequency
fp, stopband frequency fs, passband ripple dp, and stopband ripple ds.
fp and fs must be normalized with respect to the sampling frequency.
Note that the filter order is one less than the filter length.

Uses approximation algorithm described by Herrmann et al.:

O. Herrmann, L.R. Raviner, and D.S.K. Chan, Practical Design Rules for
Optimum Finite Impulse Response Low-Pass Digital Filters, Bell Syst. Tech.
Jour., 52(6):769-799, Jul./Aug. 1973.
"""

    dF = fs-fp
    a = [5.309e-3,7.114e-2,-4.761e-1,-2.66e-3,-5.941e-1,-4.278e-1]
    b = [11.01217, 0.51244]
    Dinf = log10(ds)*(a[0]*log10(dp)**2+a[1]*log10(dp)+a[2])+ \
           a[3]*log10(dp)**2+a[4]*log10(dp)+a[5]
    f = b[0]+b[1]*(log10(dp)-log10(ds))
    N1 = Dinf/dF-f*dF+1

    return int(oddround(N1))

def remlplen_kaiser(fp,fs,dp,ds):
    """
Determine the length of the low pass filter with passband frequency
fp, stopband frequency fs, passband ripple dp, and stopband ripple ds.
fp and fs must be normalized with respect to the sampling frequency.
Note that the filter order is one less than the filter length.

Uses approximation algorithm described by Kaiser:

J.F. Kaiser, Nonrecursive Digital Filter Design Using I_0-sinh Window
function, Proc. IEEE Int. Symp. Circuits and Systems, 20-23, April 1974.
"""

    dF = fs-fp
    N2 = (-20*log10(sqrt(dp*ds))-13.0)/(14.6*dF)+1.0

    return int(oddceil(N2))

def remlplen_ichige(fp,fs,dp,ds):
    """
Determine the length of the low pass filter with passband frequency
fp, stopband frequency fs, passband ripple dp, and stopband ripple ds.
fp and fs must be normalized with respect to the sampling frequency.
Note that the filter order is one less than the filter length.
Uses approximation algorithm described by Ichige et al.:
K. Ichige, M. Iwaki, and R. Ishii, Accurate Estimation of Minimum
Filter Length for Optimum FIR Digital Filters, IEEE Transactions on
Circuits and Systems, 47(10):1008-1017, October 2000.
"""
    
    dF = fs-fp
    v = lambda dF,dp:2.325*((-log10(dp))**-0.445)*dF**(-1.39)
    g = lambda fp,dF,d:(2.0/pi)*arctan(v(dF,dp)*(1.0/fp-1.0/(0.5-dF)))
    h = lambda fp,dF,c:(2.0/pi)*arctan((c/dF)*(1.0/fp-1.0/(0.5-dF)))
    Nc = ceil(1.0+(1.101/dF)*(-log10(2.0*dp))**1.1)
    Nm = (0.52/dF)*log10(dp/ds)*(-log10(dp))**0.17
    N3 = ceil(Nc*(g(fp,dF,dp)+g(0.5-dF-fp,dF,dp)+1.0)/3.0)
    DN = ceil(Nm*(h(fp,dF,1.1)-(h(0.5-dF-fp,dF,0.29)-1.0)/2.0))
    N4 = N3+DN
    
    return int(N4)

def remezord(freqs,amps,rips,Hz=1,alg='ichige'):
    """Filter parameter selection for the Remez exchange algorithm.

Description:

Calculate the parameters required by the Remez exchange algorithm to
construct a finite impulse response (FIR) filter that approximately
meets the specified design.
Inputs:

freqs --- A monotonic sequence of band edges specified in Hertz. All
elements must be non-negative and less than 1/2 the
sampling frequency as given by the Hz parameter.
amps --- A sequence containing the amplitudes of the signal to be
filtered over the various bands.
rips --- A sequence specifying the maximum ripples of each band.
alg --- Filter length approximation algorithm. May be
'herrmann', 'kaiser', or 'ichige'.

Outputs:

numtaps,bands,desired,weight -- See help for the remez function.
"""

    # Make sure the parameters are floating point numpy arrays:
    freqs = asarray(freqs,'d')
    amps = asarray(amps,'d')
    rips = asarray(rips,'d')

    # Scale ripples with respect to band amplitudes:
    rips /= (amps+(amps==0.0))

    # Normalize input frequencies with respect to sampling frequency:
    freqs /= Hz

    # Select filter length approximation algorithm:
    if alg == 'herrmann':
        remlplen = remlplen_herrmann
    elif alg == 'kaiser':
        remlplen = remlplen_kaiser
    elif alg == 'ichige':
        remlplen = remlplen_ichige
    else:
        raise ValueError('Unknown filter length approximation algorithm.')
    
    # Validate inputs:
    if any(freqs > 0.5):
        raise ValueError('Frequency band edges must not exceed the Nyquist frequency.')
    if any(freqs < 0.0):
        raise ValueError('Frequency band edges must be nonnegative.')
    if any(rips < 0.0):
        raise ValueError('Ripples must be nonnegative.')
    if len(amps) != len(rips):
        raise ValueError('Number of amplitudes must equal number of ripples.')
    if len(freqs) != 2*(len(amps)-1):
        raise ValueError('Number of band edges must equal 2*((number of amplitudes)-1)')

    # Find the longest filter length needed to implement any of the
    # low-pass or high-pass filters with the specified edges:
    f1 = freqs[0:-1:2]
    f2 = freqs[1::2]
    L = 0
    for i in range(len(amps)-1):
        L = max((L,
                 remlplen(f1[i],f2[i],rips[i],rips[i+1]),
                 remlplen(0.5-f2[i],0.5-f1[i],rips[i+1],rips[i])))

    # Cap the sequence of band edges with the limits of the digital frequency
    # range:
    bands = hstack((0.0,freqs,0.5))

    # The filter design weights correspond to the ratios between the maximum
    # ripple and all of the other ripples:
    weight = max(rips)/rips
    
    return [L,bands,amps,weight]

#######################################
# If called directly, do some example #
#######################################
if __name__=='__main__':
    pass