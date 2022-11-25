
class R:
    def __init__(self, ecg):
        self.ecg = ecg
def getR():
    a = open('database/config/read.csv','r')
    datos = a.readlines()
    return datos
def reset():
    file = open('database/config/read.csv', "w")
    file.close()
def get_R():
    a = open('database/config/read.csv','r')
    reg = a.readlines()
    return reg