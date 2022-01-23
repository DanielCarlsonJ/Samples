# This code is a sample of my work on finding alternate methods of searching gravitational wave signals for possible black hole mergers.
# After applying an FFT to find useless resonant frequencies and whitening the signal, then searching within the theoretical range of frequencies of black hole mergers
#   we can apply methods to search for possible events. In this case, a rolling standard deviation was applied to show a slight elevation in std during the event period.

#-- SET ME   Tutorial should work with most binary black hole events
#-- Default is no event selection; you MUST select one to proceed.
eventname = ''
eventname = 'GW150914' 
#eventname = 'GW151226' 
#eventname = 'LVT151012'
#eventname = 'GW170104'
# In[7]:

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
    
