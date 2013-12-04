# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 08:04:59 2013

@author: Christian Muenker
"""

import iir_basic #, fir_basic

def select(a):
    status = iir_basic.iir_basic(a)
    return status