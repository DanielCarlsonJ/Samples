# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 22:00:56 2019

@author: User 1
"""

# In[1]:

#-- SET ME   Tutorial should work with most binary black hole events
#-- Default is no event selection; you MUST select one to proceed.
eventname = ''
eventname = 'GW150914' 
#eventname = 'GW151226' 
#eventname = 'LVT151012'
#eventname = 'GW170104'

# want plots?
make_plots = 1
plottype = "png"
#plottype = "pdf"


# In[2]:

# Standard python numerical analysis imports:
import pandas as pd

import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import h5py
import json

# the IPython magic below must be commented out in the .py file, since it doesn't work there.
#get_ipython().magic(u'matplotlib inline')
#get_ipython().magic(u"config InlineBackend.figure_format = 'retina'")
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# LIGO-specific readligo.py 
import readligo as rl

# you might get a matplotlib warning here; you can ignore it.


# ### Read the event properties from a local json file (download in advance):

# In[3]:

# Read the event properties from a local json file
fnjson = "BBH_events_v3.json"
try:
    events = json.load(open(fnjson,"r"))
except IOError:
    print("Cannot find resource file "+fnjson)
    print("You can download it from https://losc.ligo.org/s/events/"+fnjson)
    print("Quitting.")
    quit()

# did the user select the eventname ?
try: 
    events[eventname]
except:
    print('You must select an eventname that is in '+fnjson+'! Quitting.')
    quit()


# In[4]:

# Extract the parameters for the desired event:
event = events[eventname]
fn_H1 = event['fn_H1']              # File name for H1 data
fn_L1 = event['fn_L1']              # File name for L1 data
fn_template = event['fn_template']  # File name for template waveform
fs = event['fs']                    # Set sampling rate
tevent = event['tevent']            # Set approximate event GPS time
fband = event['fband']              # frequency band for bandpassing signal
print("Reading in parameters for event " + event["name"])
print(event)


# ## Read in the data
# We will make use of the data, and waveform template, defined above.

# In[5]:

#----------------------------------------------------------------
# Load LIGO data from a single file.
# FIRST, define the filenames fn_H1 and fn_L1, above.
#----------------------------------------------------------------
try:
    # read in data from H1 and L1, if available:
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')
except:
    print("Cannot find data files!")
    print("You can download them from https://losc.ligo.org/s/events/"+eventname)
    print("Quitting.")
    quit()


# ## Data Gaps
# **NOTE** that in general, LIGO strain time series data has gaps (filled with NaNs) when the detectors are not taking valid ("science quality") data. Analyzing these data requires the user to 
#  <a href='https://losc.ligo.org/segments/'>loop over "segments"</a> of valid data stretches. 
# 
# **In this tutorial, for simplicity, we assume there are no data gaps - this will not work for all times!**  See the 
# <a href='https://losc.ligo.org/segments/'>notes on segments</a> for details.
# 

# ## First look at the data from H1 and L1

# In[6]:

# both H1 and L1 will have the same time vector, so:
time = time_H1
# the time sample interval (uniformly sampled!)
dt = time[1] - time[0]

# Let's look at the data and print out some stuff:

print('time_H1: len, min, mean, max = ',     len(time_H1), time_H1.min(), time_H1.mean(), time_H1.max() )
print('strain_H1: len, min, mean, max = ',     len(strain_H1), strain_H1.min(),strain_H1.mean(),strain_H1.max())
print( 'strain_L1: len, min, mean, max = ',     len(strain_L1), strain_L1.min(),strain_L1.mean(),strain_L1.max())

#What's in chan_dict?  (See also https://losc.ligo.org/tutorials/)
bits = chan_dict_H1['DATA']
print("For H1, {0} out of {1} seconds contain usable DATA".format(bits.sum(), len(bits)))
bits = chan_dict_L1['DATA']
print("For L1, {0} out of {1} seconds contain usable DATA".format(bits.sum(), len(bits)))
 


# In[7]:

# plot +- deltat seconds around the event:
# index into the strain time series for this time interval:
deltat = 5
indxt = np.where((time >= tevent-deltat) & (time < tevent+deltat))
print(tevent)

if make_plots:
    plt.figure()
    plt.plot(time[indxt]-tevent,strain_H1[indxt],'r',label='H1 strain')
    plt.plot(time[indxt]-tevent,strain_L1[indxt],'g',label='L1 strain')
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('strain')
    plt.legend(loc='lower right')
    plt.title('Advanced LIGO strain data near '+eventname)
    plt.savefig(eventname+'_strain.'+plottype)
    
    plt.show()
    
# In[8]:

make_psds = 1
if make_psds:
    # number of sample for the fast fourier transform:
    NFFT = 4*fs
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
    Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)

    # We will use interpolations of the ASDs computed above for whitening:
    psd_H1 = interp1d(freqs, Pxx_H1)
    psd_L1 = interp1d(freqs, Pxx_L1)

    # Here is an approximate, smoothed PSD for H1 during O1, with no lines. We'll use it later.    
    Pxx = (1.e-22*(18./(0.1+freqs))**2)**2+0.7e-23**2+((freqs/2000.)*4.e-23)**2
    psd_smooth = interp1d(freqs, Pxx)

if make_plots:
    # plot the ASDs, with the template overlaid:
    f_min = 20.
    f_max = 2000. 
    plt.figure(figsize=(10,8))
    plt.loglog(freqs, np.sqrt(Pxx_L1),'g',label='L1 strain')
    plt.loglog(freqs, np.sqrt(Pxx_H1),'r',label='H1 strain')
    plt.loglog(freqs, np.sqrt(Pxx),'k',label='H1 strain, O1 smooth model')
    plt.axis([f_min, f_max, 1e-24, 1e-19])
    plt.grid('on')
    plt.ylabel('ASD (strain/rtHz)')
    plt.xlabel('Freq (Hz)')
    plt.legend(loc='upper center')
    plt.title('Advanced LIGO strain data near '+eventname)
    plt.savefig(eventname+'_ASDs.'+plottype)
    
    plt.show()
    
# In[9]:

BNS_range = 1
if BNS_range:
    #-- compute the binary neutron star (BNS) detectability range

    #-- choose a detector noise power spectrum:
    f = freqs.copy()
    # get frequency step size
    df = f[2]-f[1]

    #-- constants
    # speed of light:
    clight = 2.99792458e8                # m/s
    # Newton's gravitational constant
    G = 6.67259e-11                      # m^3/kg/s^2 
    # one parsec, popular unit of astronomical distance (around 3.26 light years)
    parsec = 3.08568025e16               # m
    # solar mass
    MSol = 1.989e30                      # kg
    # solar mass in seconds (isn't relativity fun?):
    tSol = MSol*G/np.power(clight,3)     # s
    # Single-detector SNR for detection above noise background: 
    SNRdet = 8.
    # conversion from maximum range (horizon) to average range:
    Favg = 2.2648
    # mass of a typical neutron star, in solar masses:
    mNS = 1.4

    # Masses in solar masses
    m1 = m2 = mNS    
    mtot = m1+m2  # the total mass
    eta = (m1*m2)/mtot**2  # the symmetric mass ratio
    mchirp = mtot*eta**(3./5.)  # the chirp mass (FINDCHIRP, following Eqn 3.1b)

    # distance to a fiducial BNS source:
    dist = 1.0                           # in Mpc
    Dist =  dist * 1.0e6 * parsec /clight # from Mpc to seconds

    # We integrate the signal up to the frequency of the "Innermost stable circular orbit (ISCO)" 
    R_isco = 6.      # Orbital separation at ISCO, in geometric units. 6M for PN ISCO; 2.8M for EOB 
    # frequency at ISCO (end the chirp here; the merger and ringdown follow) 
    f_isco = 1./(np.power(R_isco,1.5)*np.pi*tSol*mtot)
    # minimum frequency (below which, detector noise is too high to register any signal):
    f_min = 20. # Hz
    # select the range of frequencies between f_min and fisco
    fr = np.nonzero(np.logical_and(f > f_min , f < f_isco))
    # get the frequency and spectrum in that range:
    ffr = f[fr]

    # In stationary phase approx, this is htilde(f):  
    # See FINDCHIRP Eqns 3.4, or 8.4-8.5 
    htilde = (2.*tSol/Dist)*np.power(mchirp,5./6.)*np.sqrt(5./96./np.pi)*(np.pi*tSol)
    htilde *= np.power(np.pi*tSol*ffr,-7./6.)
    htilda2 = htilde**2

    # loop over the detectors
    dets = ['H1', 'L1']
    for det in dets:
        if det is 'L1': sspec = Pxx_L1.copy()
        else:           sspec = Pxx_H1.copy()
        sspecfr = sspec[fr]
        # compute "inspiral horizon distance" for optimally oriented binary; FINDCHIRP Eqn D2:
        D_BNS = np.sqrt(4.*np.sum(htilda2/sspecfr)*df)/SNRdet
        # and the "inspiral range", averaged over source direction and orientation:
        R_BNS = D_BNS/Favg
        print(det+' BNS inspiral horizon = {0:.1f} Mpc, BNS inspiral range   = {1:.1f} Mpc'.format(D_BNS,R_BNS))
        
# In[10]:

# function to whiten data
def whiten(strain, interp_psd, dt):
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)
    freqs1 = np.linspace(0,2048.,Nt/2+1)

    # whitening: transform to freq domain, divide by asd, then transform back, 
    # taking care to get normalization right.
    hf = np.fft.rfft(strain)
    norm = 1./np.sqrt(1./(dt*2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht

whiten_data = 1
if whiten_data:
    # now whiten the data from H1 and L1, and the template (use H1 PSD):
    strain_H1_whiten = whiten(strain_H1,psd_H1,dt)
    strain_L1_whiten = whiten(strain_L1,psd_L1,dt)
    
    # We need to suppress the high frequency noise (no signal!) with some bandpassing:
    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
    strain_L1_whitenbp = filtfilt(bb, ab, strain_L1_whiten) / normalization
    
    
 # In[11]:

if make_plots:
    # index into the strain time series for this time interval:
    indxt = np.where((time >= tevent-deltat) & (time < tevent+deltat))

    # pick a shorter FTT time interval, like 1/8 of a second:
    NFFT = int(fs/8)
    # and with a lot of overlap, to resolve short-time features:
    NOVL = int(NFFT*15./16)
    # and choose a window that minimizes "spectral leakage" 
    # (https://en.wikipedia.org/wiki/Spectral_leakage)
    window = np.blackman(NFFT)

    # the right colormap is all-important! See:
    # http://matplotlib.org/examples/color/colormaps_reference.html
    # viridis seems to be the best for our purposes, but it's new; if you don't have it, you can settle for ocean.
    #spec_cmap='viridis'
    spec_cmap='ocean'

    # Plot the H1 spectrogram:
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(strain_H1[indxt], NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO H1 strain data near '+eventname)
    plt.savefig(eventname+'_H1_spectrogram.'+plottype)

    # Plot the L1 spectrogram:
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(strain_L1[indxt], NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO L1 strain data near '+eventname)
    plt.savefig(eventname+'_L1_spectrogram.'+plottype)
    
    
if make_plots:
    #  plot the whitened data, zooming in on the signal region:

    # pick a shorter FTT time interval, like 1/16 of a second:
    NFFT = int(fs/16.0)
    # and with a lot of overlap, to resolve short-time features:
    NOVL = int(NFFT*15/16.0)
    # choose a window that minimizes "spectral leakage" 
    # (https://en.wikipedia.org/wiki/Spectral_leakage)
    window = np.blackman(NFFT)

    # Plot the H1 whitened spectrogram around the signal
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(strain_H1_whiten[indxt], NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO H1 strain data near '+eventname)
    plt.savefig(eventname+'_H1_spectrogram_whitened.'+plottype)

    # Plot the L1 whitened spectrogram around the signal
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(strain_L1_whiten[indxt], NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO L1 strain data near '+eventname)
    plt.savefig(eventname+'_L1_spectrogram_whitened.'+plottype)
    
    
    
###################################

ts = time[indxt]-tevent

for x in np.logspace(1, 3, 2):
    
    xx = 10
    x = int(x)
    rolling_H1 = []
    rolling_std = []
    for i in range(len(ts)-xx):
        rolling_H1.append(np.mean(strain_H1_whiten[indxt][i:i+xx]))
        rolling_std.append(np.std(strain_H1_whiten[indxt][i:i+xx]))
        
    print(len(strain_H1_whiten[indxt][:-xx]), len(rolling_H1))
    print(np.shape(strain_H1_whiten[indxt][:-xx]), np.shape(rolling_H1))
    
    roll_std = np.std(rolling_H1)
    
    std = np.std(strain_H1_whiten[indxt][:-xx])
    
    print(xx, std, roll_std)
    
    plt.close()
    
    
    plt.plot( time[indxt][:-xx]-tevent, strain_H1_whiten[indxt][:-xx], alpha=0.5)
    plt.plot( time[indxt][:-xx]-tevent, rolling_H1, alpha=0.8)
    plt.plot( time[indxt][:-xx]-tevent, rolling_std, lw=2, alpha=1, label='Window 50')
    
    plt.ylabel('strain')
    plt.xlabel('time')
    plt.legend(loc='lower right')
    plt.title('LIGO Rolling Standard Deviation')

    
    plt.show()
    
    yy = 100
    x = int(x)
    rolling_H1_2 = []
    rolling_std_2 = []
    for i in range(len(ts)-yy):
        rolling_H1_2.append(np.mean(strain_H1_whiten[indxt][i:i+yy]))
        rolling_std_2.append(np.std(strain_H1_whiten[indxt][i:i+yy]))
        
    print(len(strain_H1_whiten[indxt][:-yy]), len(rolling_H1_2))
    print(np.shape(strain_H1_whiten[indxt][:-yy]), np.shape(rolling_H1_2))
    
    roll_std = np.std(rolling_H1_2)
    
    std = np.std(strain_H1_whiten[indxt][:-yy])
    
    print(yy, std, roll_std)
    
    plt.close()
    
    
    plt.plot( time[indxt][:-yy]-tevent, strain_H1_whiten[indxt][:-yy], alpha=0.5)
    plt.plot( time[indxt][:-yy]-tevent, rolling_H1_2, alpha=0.8)
    plt.plot( time[indxt][:-yy]-tevent, rolling_std_2, lw=2, alpha=1, label='Window 100')
    
    plt.ylabel('strain')
    plt.xlabel('time')
    plt.legend(loc='lower right')
    plt.title('LIGO Rolling Standard Deviation')

    
    plt.show()
    
    zz = 1200
    x = int(x)
    rolling_H1_3 = []
    rolling_std_3 = []
    for i in range(len(ts)-zz):
        rolling_H1_3.append(np.mean(strain_H1_whiten[indxt][i:i+zz]))
        rolling_std_3.append(np.std(strain_H1_whiten[indxt][i:i+zz]))
        
    print(len(strain_H1_whiten[indxt][:-zz]), len(rolling_H1_3))
    print(np.shape(strain_H1_whiten[indxt][:-zz]), np.shape(rolling_H1_3))
    
    roll_std = np.std(rolling_H1_3)
    
    std = np.std(strain_H1_whiten[indxt][:-zz])
    
    print(yy, std, roll_std)
    
    plt.close()
    
    
    plt.plot( time[indxt][:-zz]-tevent, strain_H1_whiten[indxt][:-zz], alpha=0.5)
    plt.plot( time[indxt][:-zz]-tevent, rolling_H1_3, alpha=0.8)
    plt.plot( time[indxt][:-zz]-tevent, rolling_std_3, lw=2, alpha=1, label='Window 1200')
    
    
    plt.ylabel('strain')
    plt.xlabel('time')
    plt.legend(loc='lower right')
    plt.title('LIGO Rolling Standard Deviation')

    
    plt.show()
    plt.savefig('LIGO_H1_ASD_WINDOWCOMPARE')
    plt.close()
#####################################
    
make_psds = 1
if make_psds:
    # number of sample for the fast fourier transform:
    NFFT = 4*fs
    Pxx_H1, freqs = mlab.psd(strain_H1_whiten, Fs = fs, NFFT = NFFT)
    Pxx_H1STD, freqs = mlab.psd(rolling_std, Fs = fs, NFFT = NFFT)
    Pxx_H1STD_2, freqs = mlab.psd(rolling_std_2, Fs = fs, NFFT = NFFT)
    Pxx_H1STD_3, freqs = mlab.psd(rolling_std_3, Fs = fs, NFFT = NFFT)

    # We will use interpolations of the ASDs computed above for whitening:
    psd_H1 = interp1d(freqs, Pxx_H1)
    psd_H1STD = interp1d(freqs, Pxx_H1STD)
    psd_H1STD_2 = interp1d(freqs, Pxx_H1STD)
    psd_H1STD_3 = interp1d(freqs, Pxx_H1STD)

    # Here is an approximate, smoothed PSD for H1 during O1, with no lines. We'll use it later.    
    Pxx = (1.e-22*(18./(0.1+freqs))**2)**2+0.7e-23**2+((freqs/2000.)*4.e-23)**2
    psd_smooth = interp1d(freqs, Pxx)

if make_plots:
    # plot the ASDs, with the template overlaid:
    f_min = 20.
    f_max = 2000. 
    plt.figure(figsize=(10,8))
    plt.loglog(freqs, np.sqrt(Pxx_H1),'b',label='H1 whitened strain')
    plt.loglog(freqs, np.sqrt(Pxx_H1STD),'r',label='H1STD Window 50/4e4')
    plt.loglog(freqs, np.sqrt(Pxx_H1STD_2),'g',label='H1STD Window 100/4e4')
    plt.loglog(freqs, np.sqrt(Pxx_H1STD_3),'y',label='H1STD Window 1200/4e4')
    plt.axis([f_min, f_max, 1e-7, 1e-1])
    plt.grid('on')
    plt.ylabel('ASD (strain/rtHz)')
    plt.xlabel('Freq (Hz)')
    plt.legend(loc='lower center')
    plt.title('Advanced LIGO strain data near '+eventname)
    plt.savefig('LIGO H1 STD Window Compare')
    
    plt.show()
    plt.close()
if make_plots:
    # index into the strain time series for this time interval:
    indxt = np.where((time >= tevent-deltat) & (time < tevent+deltat))

    # pick a shorter FTT time interval, like 1/8 of a second:
    NFFT = int(fs/8)
    # and with a lot of overlap, to resolve short-time features:
    NOVL = int(NFFT*15./16)
    # and choose a window that minimizes "spectral leakage" 
    # (https://en.wikipedia.org/wiki/Spectral_leakage)
    window = np.blackman(NFFT)

    # the right colormap is all-important! See:
    # http://matplotlib.org/examples/color/colormaps_reference.html
    # viridis seems to be the best for our purposes, but it's new; if you don't have it, you can settle for ocean.
    #spec_cmap='viridis'
    spec_cmap='ocean'

    # Plot the H1 spectrogram:
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(rolling_H1_2, NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO H1 strain data near '+eventname)
    plt.savefig(eventname+'_H1_spectrogram.'+plottype)

    # Plot the L1 spectrogram:
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(rolling_H1_2, NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO L1 strain data near '+eventname)
    plt.savefig(eventname+'_L1_spectrogram.'+plottype)
    plt.close()
    
if make_plots:
    # index into the strain time series for this time interval:
    indxt = np.where((time >= tevent-deltat) & (time < tevent+deltat))

    # pick a shorter FTT time interval, like 1/8 of a second:
    NFFT = int(fs/8)
    # and with a lot of overlap, to resolve short-time features:
    NOVL = int(NFFT*15./16)
    # and choose a window that minimizes "spectral leakage" 
    # (https://en.wikipedia.org/wiki/Spectral_leakage)
    window = np.blackman(NFFT)

    # the right colormap is all-important! See:
    # http://matplotlib.org/examples/color/colormaps_reference.html
    # viridis seems to be the best for our purposes, but it's new; if you don't have it, you can settle for ocean.
    #spec_cmap='viridis'
    spec_cmap='ocean'

    # Plot the H1 spectrogram:
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(rolling_H1, NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO H1 strain data near '+eventname)
    plt.savefig(eventname+'_H1_spectrogram.'+plottype)

    # Plot the L1 spectrogram:
    plt.figure(figsize=(10,6))
    spec_H1, freqs, bins, im = plt.specgram(rolling_H1, NFFT=NFFT, Fs=fs, window=window, 
                                            noverlap=NOVL, cmap=spec_cmap, xextent=[-deltat,deltat])
    plt.xlabel('time (s) since '+str(tevent))
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.axis([-deltat, deltat, 0, 2000])
    plt.title('aLIGO L1 strain data near '+eventname)
    plt.savefig(eventname+'_L1_spectrogram.'+plottype)


###################################

deltat = .2
indxt = np.where((time >= tevent-deltat) & (time < tevent+deltat))
print(tevent)

ts = time[indxt]-tevent

for x in np.logspace(1, 3, 2):
    
    xx = 1200
    x = int(x)
    rolling_H1 = []
    rolling_std = []
    for i in range(len(ts)-xx):
        rolling_H1.append(np.mean(strain_H1_whiten[indxt][i:i+xx]))
        rolling_std.append(np.std(strain_H1_whiten[indxt][i:i+xx]))
        
    print(len(strain_H1_whiten[indxt][:-xx]), len(rolling_H1))
    print(np.shape(strain_H1_whiten[indxt][:-xx]), np.shape(rolling_H1))
    
    roll_std = np.std(rolling_H1)
    
    std = np.std(strain_H1_whiten[indxt][:-xx])
    
    print(xx, std, roll_std)
    
    plt.close()
    
    
    plt.plot( time[indxt][:-xx]-tevent, strain_H1_whiten[indxt][:-xx], alpha=0.5)
    plt.plot( time[indxt][:-xx]-tevent, rolling_H1, alpha=0.8)
    plt.plot( time[indxt][:-xx]-tevent, rolling_std, lw=2, alpha=1, label='Event Time')
    
    plt.ylabel('strain')
    plt.xlabel('time')
    plt.legend(loc='lower right')
    plt.title('LIGO Rolling Standard Deviation')
    
    plt.show()
    
deltat = .2
indxt = np.where((time >= tevent-deltat+3) & (time < tevent+deltat+3))
print(tevent)

ts = time[indxt]-tevent

for x in np.logspace(1, 3, 2):
    
    yy = 1200
    x = int(x)
    rolling_H1_2 = []
    rolling_std_2 = []
    for i in range(len(ts)-yy):
        rolling_H1_2.append(np.mean(strain_H1_whiten[indxt][i:i+yy]))
        rolling_std_2.append(np.std(strain_H1_whiten[indxt][i:i+yy]))
        
    print(len(strain_H1_whiten[indxt][:-yy]), len(rolling_H1_2))
    print(np.shape(strain_H1_whiten[indxt][:-yy]), np.shape(rolling_H1_2))
    
    roll_std = np.std(rolling_H1_2)
    
    std = np.std(strain_H1_whiten[indxt][:-yy])
    
    print(yy, std, roll_std)
    
    plt.close()
    
    
    plt.plot( time[indxt][:-yy]-tevent, strain_H1_whiten[indxt][:-yy], alpha=0.5)
    plt.plot( time[indxt][:-yy]-tevent, rolling_H1_2, alpha=0.8)
    plt.plot( time[indxt][:-yy]-tevent, rolling_std_2, lw=2, alpha=1, label='Event Time +3')
    
    plt.ylabel('strain')
    plt.xlabel('time')
    plt.legend(loc='lower right')
    plt.title('LIGO Rolling Standard Deviation')
    
    plt.show()
    
    plt.show()
    
deltat = .2
indxt = np.where((time >= tevent-deltat-3) & (time < tevent+deltat-3))
print(tevent)

ts = time[indxt]-tevent

for x in np.logspace(1, 3, 2):
    
    zz = 1200
    x = int(x)
    rolling_H1_3 = []
    rolling_std_3 = []
    for i in range(len(ts)-zz):
        rolling_H1_3.append(np.mean(strain_H1_whiten[indxt][i:i+zz]))
        rolling_std_3.append(np.std(strain_H1_whiten[indxt][i:i+zz]))
        
    print(len(strain_H1_whiten[indxt][:-zz]), len(rolling_H1_3))
    print(np.shape(strain_H1_whiten[indxt][:-zz]), np.shape(rolling_H1_3))
    
    roll_std = np.std(rolling_H1_3)
    
    std = np.std(strain_H1_whiten[indxt][:-zz])
    
    print(zz, std, roll_std)
    
    plt.close()
    
    plt.plot( time[indxt][:-zz]-tevent, strain_H1_whiten[indxt][:-zz], alpha=0.5)
    plt.plot( time[indxt][:-zz]-tevent, rolling_H1_3, alpha=0.8)
    plt.plot( time[indxt][:-zz]-tevent, rolling_std_3, lw=2, alpha=1, label='Event Time -3')
    
    plt.ylabel('strain')
    plt.xlabel('time')
    plt.legend(loc='lower right')
    plt.title('LIGO Rolling Standard Deviation')
    
    plt.show()
    
    plt.show()
    
###########################################
   
make_psds = 1
if make_psds:
    # number of sample for the fast fourier transform:
    NFFT = 4*fs
    Pxx_H1, freqs = mlab.psd(strain_H1_whiten, Fs = fs, NFFT = NFFT)
    Pxx_H1STD, freqs = mlab.psd(rolling_std, Fs = fs, NFFT = NFFT)
    Pxx_H1STD_2, freqs = mlab.psd(rolling_std_2, Fs = fs, NFFT = NFFT)
    Pxx_H1STD_3, freqs = mlab.psd(rolling_std_3, Fs = fs, NFFT = NFFT)

    # We will use interpolations of the ASDs computed above for whitening:
    psd_H1 = interp1d(freqs, Pxx_H1)
    psd_H1STD = interp1d(freqs, Pxx_H1STD)
    psd_H1STD_2 = interp1d(freqs, Pxx_H1STD)
    psd_H1STD_3 = interp1d(freqs, Pxx_H1STD)

    # Here is an approximate, smoothed PSD for H1 during O1, with no lines. We'll use it later.    
    Pxx = (1.e-22*(18./(0.1+freqs))**2)**2+0.7e-23**2+((freqs/2000.)*4.e-23)**2
    psd_smooth = interp1d(freqs, Pxx)

if make_plots:
    # plot the ASDs, with the template overlaid:
    f_min = 0.
    f_max = 10000. 
    plt.figure(figsize=(10,8))
    plt.loglog(freqs, np.sqrt(Pxx_H1),'b',label='H1 whitened strain')
    plt.loglog(freqs, np.sqrt(Pxx_H1STD),'r',label='H1STD t Window 0.2')
    plt.loglog(freqs, np.sqrt(Pxx_H1STD_2),'g',label='H1STD t+3')
    plt.loglog(freqs, np.sqrt(Pxx_H1STD_3),'y',label='H1STD t-3')
    plt.axis([f_min, f_max, 1e-6, .5*1e-3])
    plt.grid('on')
    plt.ylabel('ASD (strain/rtHz)')
    plt.xlabel('Freq (Hz)')
    plt.legend(loc='upper center')
    plt.title('Advanced LIGO strain data near '+eventname)
    plt.savefig('LIGO H1 STD Time Compare')
    
    plt.show()
    




    
#Biweight midvariance
#STD of ASD of H1 whitened
#adjust window of ASD of H1STD whitened
#adjust time window (nothing)
    
#Cover science in ppt
    