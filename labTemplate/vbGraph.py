#!/usr/bin/env python2
# coding=utf8

import argparse
from matplotlib import rc, use
import pylab
import numpy
"""
Copyright (c) 2013, Quincy Lam 
All rights reserved. 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met: 

 * Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer. 
 * Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the 
   documentation and/or other materials provided with the distribution. 
 * Neither the name of  nor the names of its contributors may be used to 
   endorse or promote products derived from this software without specific 
   prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE. 
"""

font = {'family': 'FreeSerif'}
savefig = {'dpi': 300, 'extension': 'pdf'}
rc('font', **font)
rc('savefig', **savefig)

f = pylab.figure(figsize=(3,2), dpi=150)
a = f.gca()
a.set_xlabel(ur"Time (s) $\rightarrow$", fontsize=10)
a.set_xscale("linear")
a.set_ylabel(ur"Velocity (ms$^{-1}$) $\rightarrow$", fontsize=10)
a.set_yscale("linear")
a.set_title(ur"$\mathit{You}$ fail $\mathtt{math}$ $\mathcal{FOREVER}$", fontsize=12)
a.grid(True, color="0.9", linewidth=0.5, linestyle="-")
a.set_axisbelow(True)
a.tick_params(direction='out', top='off', right='off')

a.plot([0,1,2,3.05,4,5],[5,0,7,0.2,6,7.5], markerfacecolor="none", marker="o", linestyle="")
a.errorbar([0,1,2,3.05,4,5],[5,0,7,0.2,6,7.5],xerr=[.2,.2,.2,.2,.2,.2], yerr=[2,3,3.5,4,4.6,5], linestyle='', color='black')
a.plot([1,3,4,5],[7,7.2,6.01,5], marker="*")
a.plot(numpy.arange(0,6), 3*numpy.sin(numpy.arange(0,6) - numpy.pi), linestyle="-", color="0.6")

f.tight_layout()
f.savefig('matplotlibTest')
pylab.close()
# WIP
