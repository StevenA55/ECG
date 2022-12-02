from scipy.io import loadmat
from scipy import signal
import numpy as np
#import matplotlib.pyplot as plt
from pandas import Series
from mat4py import loadmat
import pandas as pd
file = 'C:/Users/57310/Documents/DABM/Proyecto final/database/100m.mat'
x = loadmat(file)
ecg = x['val']
ecg = ecg[0]
ECG= np.transpose(ecg)
size = np.size(ECG)
fs = 360
ts =1/fs
t = np.linspace(0, np.size(ecg),np.size(ecg))*ts