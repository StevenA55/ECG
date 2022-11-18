# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from mat4py import loadmat
x = loadmat('101m.mat')
ecg = x['val']
ecg = ecg[0]
ecg= np.transpose(ecg)
fs = 360
ts = 1/fs
t = np.linspace(0, np.size(ecg),np.size(ecg))*ts
plt.plot(t,ecg)
plt.show()
