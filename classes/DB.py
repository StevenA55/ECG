import numpy as np
from mat4py import loadmat
class DB:
    def __init__(self, t, ecg, data):
        self.t = t
        self.ecg = ecg
        self.data = data
def getcb_DB():
    a = open('database/config/cb_DB.csv','r')
    cb = a.readlines()
    return cb
def data(select_DB):
        file = 'database/'+select_DB
        x = loadmat(file)
        ecg = x['val']
        ecg = ecg[0]
        ecg= np.transpose(ecg)
        fs = 360
        ts = 1/fs
        t = np.linspace(0, np.size(ecg),np.size(ecg))*ts
        return t, ecg