from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import pyqtgraph as pg
import sys
import os
import numpy as np
from os import path
import librosa
from librosa import display
import matplotlib.pyplot as plt
import scipy
from scipy.fft import rfft, rfftfreq,irfft
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QLabel
import copy
import sounddevice as sd
import time
import datetime
from scipy.io.wavfile import write
import math

THIS_FOLDER= path.dirname(path.abspath(__file__))
FORM_CLASS,_=loadUiType(path.join(THIS_FOLDER, "equilizer.ui"))

class MainApp(QtWidgets.QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        self.intial_conditions()

    

    def handle_UI(self):
        _translate = QtCore.QCoreApplication.translate
        self.p1 = self.spect_view.addPlot()
        self.hist = pg.HistogramLUTItem()
        self.spect_view.addItem(self.hist)
        self.hide_spect.setChecked(True)
        self.spect_view.addItem(self.hist)
        self.hist.gradient.restoreState(
        {'mode': 'hsv',
         'ticks': [(0.5, (0, 182, 188, 255)),
                   (1.0, (246, 111, 0, 255)),
                   (0.0, (75, 0, 113, 255))]})        
       
        ###################################events############################
        self.open.triggered.connect(lambda: self.read_file())
        self.slider1.valueChanged.connect(lambda:self.slider_value())
        self.slider2.valueChanged.connect(lambda:self.slider_value())
        self.slider3.valueChanged.connect(lambda:self.slider_value())
        self.slider4.valueChanged.connect(lambda:self.slider_value())
        self.slider5.valueChanged.connect(lambda:self.slider_value())
        self.slider6.valueChanged.connect(lambda:self.slider_value())
        self.slider7.valueChanged.connect(lambda:self.slider_value())
        self.slider8.valueChanged.connect(lambda:self.slider_value())
        self.slider9.valueChanged.connect(lambda:self.slider_value())
        self.slider10.valueChanged.connect(lambda:self.slider_value())

        self.zoom_in.clicked.connect(lambda:self.ZOOM("i"))
        self.zoom_out.clicked.connect(lambda:self.ZOOM("o"))

        self.save_new.triggered.connect(lambda: self.save_audio())
       
        self.original.plotItem.vb.setLimits(xMin=0)
        self.test.plotItem.vb.setLimits(xMin=0)

        self.right.clicked.connect(lambda :self.SCROLL("r"))
        self.left.clicked.connect(lambda :self.SCROLL("l"))        
        self.up.clicked.connect(lambda :self.SCROLL("u"))
        self.down.clicked.connect(lambda :self.SCROLL("d"))

        self.spinBox.valueChanged.connect(lambda:self.speed_control())
        self.new_file.triggered.connect(open_otherwindow)
        self.save_pdf.triggered.connect(lambda:self.savepdf())
        self.hide_spect.stateChanged.connect(lambda: self.hide())
        self.reset.triggered.connect(lambda: self.clearall())

        self.close.triggered.connect(sys.exit)


        ##############################shortcuts###############################3

        self.zoom_in.setShortcut (_translate("MainWindow", "Ctrl++"))
        self.zoom_out.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.save_pdf.setShortcut(_translate("MainWindow", "Ctrl+s"))
        self.save_new.setShortcut(_translate("MainWindow", "Ctrl+u"))
        self.new_file.setShortcut(_translate("MainWindow", "Ctrl+n"))
        self.open.setShortcut(_translate("MainWindow", "Ctrl+o"))
        self.reset.setShortcut(_translate("MainWindow", "Ctrl+r"))
        self.close.setShortcut(_translate("MainWindow", "esc"))

    def intial_conditions(self):
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(50)
        self.timer1.setInterval(50)
        self.sliders=[self.slider1,self.slider2,self.slider3,self.slider4,self.slider5,self.slider6,self.slider7,self.slider8,self.slider9,self.slider10]
        for i in range (len(self.sliders)):
            self.sliders[i].setEnabled(False)   


    def read_file (self):
        
        load_file= QtGui.QFileDialog.getOpenFileName( self, 'Choose File', THIS_FOLDER ,"wav(*.wav)")
        path=load_file[0]

        self.samples, self.fs = librosa.load(path,sr=None)   #Getting the data and sampling rate (fs)
        self.duration=np.arange(len(self.samples))/self.fs      #The time axis of the data
        self.N=len(self.samples)    #number of samples 

        for i in range (len(self.sliders)):
            self.sliders[i].setEnabled(True)                             
        
        self.play(1)
        self.st_x1=0
        self.timer1.timeout.connect(lambda:self.update(1))
        self.timer1.start()

        #self.original.plot(x=self.duration,y=self.samples)  #Original Plot     

        ############# Fourier ##############

        self.yf = rfft(self.samples)    
        self.magnitude=np.abs(self.yf) 
        self.phase=np.angle(self.yf)        
        self.freq = rfftfreq(self.N, 1 / self.fs)   #frequency axis

        self.slider_value()  #Intializing the sliders values


    def slider_value(self):
        self.sliders_values=[]
        for i in range (len(self.sliders)):
            self.sliders_values.append(self.sliders[i].value())      
        self.equalized()        #Intializing the equalized signal
     
        
    def equalized (self):
        data=copy.deepcopy(self.magnitude) #Copy of magnitudes
        bands=10
        length=len(self.freq)/2

        for i in range(bands): #getting gains
            #if 0==i:
             #   data[int(((i) /bands) * length) : int((((i+1) / bands) * length)+1)]=data[int(((i) / bands) * length) : int((((i+1) / bands) * length)+1)]*self.sliders_values[i]
            #else:
            data[int((((i) / bands) * length)+1) : int((((i+1) / bands) * length)+1)]=data[int((((i) / bands) * length)+1) : int((((i+1) / bands) * length)+1)]*self.sliders_values[i]
   

        datap=np.multiply(data , np.exp(1j*self.phase))  #multipling by phase
       
        self.equalized_audio = irfft(datap) #inverse fft 

        self.test.clear()   ### refreshing plot
        self.play(2)
        self.st_x2=0
        self.timer2.timeout.connect(lambda:self.update(2))
        self.timer2.start()
        self.plot_spect()   #spectrogram function
        
        
        
    def update(self,timer):
        if timer == 1:
            if self.st_x1>len(self.duration):
                self.st_x1=250   
            duration=self.duration[:self.st_x1]
            samples=self.samples[:self.st_x1]
            self.st_x1+=250
            self.original.plot(duration,samples,pen=pg.mkPen('b', width=1))

        elif timer == 2:
            if self.st_x2>len(self.duration):
                self.st_x2=250    
            duration=self.duration[:self.st_x2]
            equalized_audio=self.equalized_audio[:self.st_x2]
            self.st_x2+=250
            self.test.plot(duration,equalized_audio,pen=pg.mkPen('b', width=1))
    QtCore.QCoreApplication.processEvents()

    def speed_control(self):
        self.timer1.setInterval(self.spinBox.value())
        self.timer1.timeout.connect(self.update1)
        self.timer1.start()
        self.timer2.setInterval(self.spinBox.value())
        self.timer2.timeout.connect(self.update2)
        self.timer2.start()
        
        
        ###########################################spectrogram#####################  
    def plot_spect(self):
                
        f, t, Sxx = scipy.signal.spectrogram(self.equalized_audio,self.fs)
        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.mkQApp()  
        img = pg.ImageItem()
        self.hist.setImageItem(img)
        self.hist.setLevels(np.min(Sxx), np.max(Sxx)) 
        img.setImage(Sxx)
        img.scale(t[-1],
          f[-1])
        self.p1.setLabel('bottom', "Time", units='s')
        self.p1.setLabel('left', "Frequency", units='Hz')
        self.p1.addItem(img)
        self.p1.show()
        
        
    def play(self,audio):
        if audio == 1:
            sd.play(self.samples, self.fs)
        elif audio == 2:
            sd.play(self.equalized_audio, self.fs)   

        QtCore.QCoreApplication.processEvents()
        #########################zoom_in#########################
    def ZOOM (self,zoom):
        if zoom == "i":
            self.original.plotItem.getViewBox().scaleBy(y=0.9,x=0.9)
            self.test.plotItem.getViewBox().scaleBy(y=0.9,x=0.9)
        if zoom == "o":
            self.original.plotItem.getViewBox().scaleBy(y=1/0.9,x=1/0.9)
            self.test.plotItem.getViewBox().scaleBy(y=1/0.9,x=1/0.9)

        ########################## scrolling ######################
   
    def SCROLL(self,scroll):

        if scroll == "r":
            self.original.plotItem.getViewBox().translateBy(x=0.1)
            self.test.plotItem.getViewBox().translateBy(x=0.1)
            
        elif scroll == "l":
            self.original.plotItem.getViewBox().translateBy(x=-0.1)
            self.test.plotItem.getViewBox().translateBy(x=-0.1)
       
        elif scroll == "u":
            self.original.plotItem.getViewBox().translateBy(y=0.1)
            self.test.plotItem.getViewBox().translateBy(y=0.1)
       
        elif scroll == "d":
            self.original.plotItem.getViewBox().translateBy(y=-0.1)
            self.test.plotItem.getViewBox().translateBy(y=-0.1)
       

        ##########################hide spectrogram################################3
    def hide(self):
         if (self.hide_spect.isChecked()):
             self.spect_view.show()
             self.label.show()
         else:
             self.spect_view.hide()    
             self.label.hide()
        #########################clearall####################################3
    def clearall(self):
        self.timer1.stop()
        self.timer2.stop()
        self.original.clear()
        self.test.clear()
        self.p1.clear()

        for i in range (len(self.sliders)):
            self.sliders[i].setValue(1)
        ##############################savepdf#####################################
    def savepdf(self):
        fig=plt.figure()
        plt.subplot(3, 1, 1)
        plt.plot(self.duration,self.samples,color="green", linewidth=1,scalex=True)
        plt.subplot(3, 1, 2)
        plt.plot(self.duration,self.equalized_audio,color="red", linewidth=1,scalex=True)
        plt.subplot(3, 1, 3)
        f, t, Sxx = scipy.signal.spectrogram(self.equalized_audio,self.fs)
        plt.pcolormesh(t, f, Sxx, shading='gouraud')
        plt.tight_layout()

        fig.savefig(os.path.join(THIS_FOLDER,"New.pdf"))


     

    def save_audio(self):
        #normalized_tone = np.int16((self.equalized_audio / self.equalized_audio.max()) * 32767)
        write(os.path.join(THIS_FOLDER,"New audio .wav"), self.fs, self.equalized_audio )


def open_otherwindow():
    window = MainApp()
    window.show()

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window= MainApp()
    window.show()  
    app.exec_()
    
     


if __name__ == '__main__':
    main()