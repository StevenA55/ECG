from scipy.io import loadmat
from scipy import signal
import numpy as np
#import matplotlib.pyplot as plt
from pandas import Series
from mat4py import loadmat
import pandas as pd

def BandPassECG(Fs,select_DB):
    # Import the signal
    file = 'database/'+select_DB
    x = loadmat(file)
    ecg = x['val']
    ecg = ecg[0]
    ECG= np.transpose(ecg)
    # Implementing the Butterworth BP filter
    W1     = 5*2/Fs                                    # --> 5 Hz cutt-off (high-pass) and Normalize by Sample Rate
    W2     = 15*2/Fs                                   # --> 15 Hz cutt-off (low-pass) and Normalize by Sample Rate
    b, a   = signal.butter(4, [W1,W2], 'bandpass')     # --> create b,a coefficients , since this is IIR we need both b and a coefficients
    ECG    = np.asarray(ECG)                           # --> let's convert the ECG to a numpy array, this makes it possible to perform vector operations 
    ECG    = np.squeeze(ECG)                           # --> squeeze
    ECG_BP = signal.filtfilt(b,a,ECG)    # --> filtering: note we use a filtfilt that compensates for the delay
    return ECG_BP,ECG

def Differentiate(ECG):
    '''
    Compute single difference of the signal ECG
    '''
    ECG_df  = np.diff(ECG)
    ECG_sq  = np.power(ECG_df,2)
    return np.insert(ECG_sq,0, ECG_sq[0])

def MovingAverage(ECG,N=30):
    '''
    Compute moving average of signal ECG with a rectangular window of N
    '''
    window  = np.ones((1,N))/N
    ECG_ma  = np.convolve(np.squeeze(ECG),np.squeeze(window))
    return ECG_ma

def QRSpeaks(ECG,Fs):
    '''
    Finds peaks in a smoothed signal ECG and sampling freq Fs.
    '''
    peaks, _  = signal.find_peaks(ECG, height=np.mean(ECG), distance=round(Fs*0.200))
    return peaks
def QRS(select_DB):
    # Load and BP the Signal
    Fs =360
    #Path ='C:/Users/57310/Documents/DABM/Proyecto final/database/101m.mat'
    
    ECG_BP,ECG_raw = BandPassECG(Fs,select_DB)
    # Create Series and plot the first 10 seconds
    ts_raw = Series(np.squeeze(ECG_raw[:10*Fs] - np.mean(ECG_raw)), index=np.arange(ECG_raw[:10*Fs].shape[0])/Fs)
    ts_BP = Series(np.squeeze(ECG_BP[:10*Fs]), index=np.arange(ECG_raw[:10*Fs].shape[0])/Fs)
    # BP Filter
    ECG_BP,ECG_raw = BandPassECG(Fs,select_DB)
    
    # Difference Filter
    ECG_df = Differentiate(ECG_BP)
    
    # Moving Average
    ECG_ma = MovingAverage(ECG_df)
    
    # QRS peaks
    QRS = QRSpeaks(ECG_ma,Fs)
    
    # Plots
    #fig = plt.figure(frameon="False") 
    #plt.plot(np.arange(ECG_raw.shape[0])/Fs,ECG_raw,color='y',label='ECG')
    #plt.vlines(x=(QRS-15)/Fs,ymin=np.min(ECG_raw),ymax=np.max(ECG_raw),linestyles='dashed',color='y', label='QRS',linewidth=2.0)
    #plt.ylabel('Amp'); plt.xlabel('Time[S]'); plt.legend()
    #plt.tight_layout(); plt.show()
    #fig.savefig('QRS_pks.png', transparent=True)
    
    #ECG_df = Differentiate(ECG_BP)
    #ts_df = Series(np.squeeze(ECG_df[:10*Fs]), index=np.arange(ECG_raw[:10*Fs].shape[0])/Fs)
    #PAN1 = ts_df.tolist()
    #fig = plt.figure(frameon="False"); ts_df.plot(style='r--', label='ECG-differentiate',linewidth=2.0); 
    #ts_BP.plot(style='y',label='ECG-BP')
    #plt.ylabel('Amp'); plt.xlabel('Time[S]',); plt.legend()
    #plt.tight_layout(); plt.show()
    #fig.savefig('ECG_df.png', transparent=True)
    
    #ECG_ma = MovingAverage(ECG_df)
    ts_ma = Series(np.squeeze(ECG_ma[:10*Fs]), index=np.arange(ECG_raw[:10*Fs].shape[0])/Fs)
    PAN = ts_ma.tolist()
    print(QRS)
    #fig = plt.figure(frameon="False"); ts_df.plot(style='y',label='ECG-DF') 
    #ts_ma.plot(style='r-', label='ECG-MA',linewidth=2.0)
    #plt.ylabel('Amp'); plt.xlabel('Time[S]',); plt.legend()
    #plt.tight_layout(); plt.show()
    #fig.savefig('ECG_ma.png', transparent=True)
    return PAN