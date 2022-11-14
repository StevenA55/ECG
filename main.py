# -*- coding: utf-8 -*-
import sys
import icons_rc
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QPoint
import pyqtgraph as pg
import numpy as np

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('interface.ui', self) # Para no convertirlo
        # Elimina la barra de título
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        # SizeGrip (redimensionar)
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Mover ventana
        self.header_frame.mouseMoveEvent= self.mover_ventana
        # Acceder a las páginas
        self.bt_inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cero))
        self.bt_ECG.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_uno))
        self.bt_registro.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dos))
        self.bt_BD.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_tres))
        self.bt_who.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cuatro))
        self.bt_creditos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cinco))
        # Control barra de títulos
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())
        self.bt_restaurar.hide()
        # Menu lateral
        self.bt_menu.clicked.connect(self.mover_menu)
        self.bt_menu2.clicked.connect(self.mover_menu)
        self.bt_menu2.hide()
        # Control connect
        self.serial = QSerialPort()
        self.bt_update.clicked.connect(self.read_ports)
        self.bt_connect.clicked.connect(self.serial_connect)
        self.bt_disconnect.clicked.connect(self.serial_disconnect)
        self.serial.readyRead.connect(self.read_data)
        self.x = list(np.linspace(0,100,100))
        self.y = list(np.linspace(0,0,100))
        # Grafica
        pg.setConfigOption('background', '#09050d')
        pg.setConfigOption('foreground', '#ffffff')
        self.plt = pg.PlotWidget(title = 'ECG')
        self.graph_layout.addWidget(self.plt)
        self.read_ports()


    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_menu(self):
        if True:
            width =self.slide_menu_container.width()
            normal = 0
            if width == 0:
                extender = 210
                self.bt_menu.hide()
                self.bt_menu2.show()
            else:
                extender = normal
                self.bt_menu2.hide()
                self.bt_menu.show()
        self.animation = QPropertyAnimation(self.slide_menu_container, b'minimumWidth')
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(extender)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        
    def control_bt_minimizar(self):
        self.showMinimized()
        
    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()
        
    def control_bt_maximizar(self):
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()    
        
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize) 
        
    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()     
        if event.globalPos().y() <= 20:
            self.showMaximized()
            self.bt_maximizar.hide()
            self.bt_restaurar.show()
        else:
            self.showNormal()
            self.bt_restaurar.hide()
            self.bt_maximizar.show()

    def read_ports(self):
        self.baudrates = ['9600']
        portList =[]
        ports = QSerialPortInfo().availablePorts()
        for i in ports:
            portList.append(i.portName())
        
        self.cb_list_ports.clear()
        self.cb_list_baudrates.clear()
        self.cb_list_ports.addItems(portList)
        self.cb_list_baudrates.addItems(self.baudrates)
        self.cb_list_baudrates.setCurrentText('9600')
        
    def serial_connect(self):
        #self.serial.waitForReadyRead(100)
        self.plt.clear()
        self.port = self.cb_list_ports.currentText()
        self.baud = self.cb_list_baudrates.currentText()
        self.serial.setBaudRate(int(self.baud))
        self.serial.setPortName(self.port)
        self.serial.open(QIODevice.ReadWrite)
        
    def serial_disconnect(self):
        self.serial.close()
        self.plt.clear()
        
    def read_data(self):
        if not self.serial.canReadLine(): return
        rx = self.serial.readLine()
        x = str(rx, 'utf-8').strip()
        x = float(x)
        #print(x)
        self.y = self.y[1:]
        self.y.append(x)
        self.plt.clear()
        self.plt.plot(self.x, self.y, pen=pg.mkPen('#da0037', width=2))
        
    def send_data(self, data):
        data = data + "\n"
        #print(data)
        if self.serial.isOpen():
            self.serial.write(data.encode())

if __name__ == "__main__":
     app = QApplication(sys.argv)
     mi_app = VentanaPrincipal()
     mi_app.show()
     sys.exit(app.exec_())