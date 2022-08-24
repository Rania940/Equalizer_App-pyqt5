from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5 import QtMultimediaWidgets
from PyQt5.uic import loadUiType
import sys
import os
from os import path
from scipy import signal
import matplotlib as s
import matplotlib.pyplot
import numpy as np
import pyqtgraph as pg
import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import soundfile as sf



sample_rate, samples = wavfile.read(r'c:/Users/Noran ElShahat/Equalizer/sound signal.wav')
f, t, Sxx,x = s.pyplot.specgram(samples,sample_rate)
s.pyplot.show()



class Ui_mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setupUi(self, MainWindow):
        self.sample_rate,self.samples = wavfile.read(r'c:/Users/Noran ElShahat/Equalizer/sound signal.wav')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.new = QtWidgets.QPushButton(self.centralwidget)
        self.new.setGeometry(QtCore.QRect(0, 0, 93, 28))
        self.new.setObjectName("new")
        
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(550, 470, 93, 28))
        self.reset.setObjectName("reset")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(660, 470, 93, 28))
        self.save.setObjectName("save")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 250, 701, 181))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.slider1 = QtWidgets.QSlider(self.widget)
        self.slider1.setSliderPosition(40)
        self.slider1.setOrientation(QtCore.Qt.Vertical)
        self.slider1.setObjectName("slider1")
        self.horizontalLayout.addWidget(self.slider1)
        self.slider2 = QtWidgets.QSlider(self.widget)
        self.slider2.setSliderPosition(40)
        self.slider2.setOrientation(QtCore.Qt.Vertical)
        self.slider2.setObjectName("slider2")
        self.horizontalLayout.addWidget(self.slider2)
        self.slider3 = QtWidgets.QSlider(self.widget)
        self.slider3.setSliderPosition(40)
        self.slider3.setOrientation(QtCore.Qt.Vertical)
        self.slider3.setObjectName("slider3")
        self.horizontalLayout.addWidget(self.slider3)
        self.slider4 = QtWidgets.QSlider(self.widget)
        self.slider4.setSliderPosition(40)
        self.slider4.setOrientation(QtCore.Qt.Vertical)
        self.slider4.setObjectName("slider4")
        
        self.horizontalLayout.addWidget(self.slider4)
        self.slider5 = QtWidgets.QSlider(self.widget)
        self.slider5.setSliderPosition(40)
        self.slider5.setOrientation(QtCore.Qt.Vertical)
        self.slider5.setObjectName("slider5")
        self.horizontalLayout.addWidget(self.slider5)
        self.slider6 = QtWidgets.QSlider(self.widget)
        self.slider6.setSliderPosition(40)
        self.slider6.setOrientation(QtCore.Qt.Vertical)
        self.slider6.setObjectName("slider6")
        self.horizontalLayout.addWidget(self.slider6)
        self.slider7 = QtWidgets.QSlider(self.widget)
        self.slider7.setSliderPosition(40)
        self.slider7.setOrientation(QtCore.Qt.Vertical)
        self.slider7.setObjectName("slider7")
        self.horizontalLayout.addWidget(self.slider7)
        self.slider8 = QtWidgets.QSlider(self.widget)
        self.slider8.setSliderPosition(40)
        self.slider8.setOrientation(QtCore.Qt.Vertical)
        self.slider8.setObjectName("slider8")
        self.horizontalLayout.addWidget(self.slider8)
        self.slider9 = QtWidgets.QSlider(self.widget)
        self.slider9.setSliderPosition(40)
        self.slider9.setOrientation(QtCore.Qt.Vertical)
        self.slider9.setObjectName("slider9")
        self.horizontalLayout.addWidget(self.slider9)
        self.slider10 = QtWidgets.QSlider(self.widget)
        self.slider10.setSliderPosition(40)
        self.slider10.setOrientation(QtCore.Qt.Vertical)
        self.slider10.setObjectName("slider10")
        self.horizontalLayout.addWidget(self.slider10)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(50, 40, 701, 194))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.spect_view =pg.GraphicsLayoutWidget(self.widget1)
        self.spect_view.setObjectName("spect_view")
        self.horizontalLayout_2.addWidget(self.spect_view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menufile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.save.clicked.connect(lambda:self.plot())
        self.p1 = self.spect_view.addPlot()
        self.hist = pg.HistogramLUTItem()
        self.spect_view.addItem(self.hist)
        
        self.reset.clicked.connect(lambda: self.playSound())
        self.new.clicked.connect(open_otherwindow)
        
####################moheb#################################nouran##############
        
    def plot(self):
                
        f, t, Sxx = signal.spectrogram(self.samples,self.sample_rate)

        pg.setConfigOptions(imageAxisOrder='row-major')
        pg.mkQApp()  
        img = pg.ImageItem()
        self.hist.setImageItem(img)
        self.spect_view.addItem(self.hist)
        self.hist.setLevels(np.min(Sxx), np.max(Sxx))
        self.hist.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(0.5, (0, 182, 188, 255)),
                   (1.0, (246, 111, 0, 255)),
                   (0.0, (75, 0, 113, 255))]})        
        
        img.setImage(Sxx)
        img.scale(t[-1]/np.size(Sxx, axis=1),
          f[-1]/np.size(Sxx, axis=0))
        self.p1.setLabel('bottom', "Time", units='s')
        self.p1.setLabel('left', "Frequency", units='Hz')
        self.p1.addItem(img)
        self.p1.show()



        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.new.setText(_translate("MainWindow","New"))
        self.reset.setText(_translate("MainWindow", "Play"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Spectrogram"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.save.clicked.connect(lambda:self.plot())  
        
    def playSound(self):
        filename = 'C:/Users/Noran ElShahat/Equalizer/air_spray1.wav'
        data, fs = sf.read('C:/Users/Noran ElShahat/Equalizer/air_spray1.wav', dtype='float32')  
        sd.play(data, fs)
        status = sd.wait()
        


        
def open_otherwindow():
    ui = Ui_mainwindow()
    ui.show()
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_mainwindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())