# -*- coding: utf-8 -*- 
#PyQt5-LAB1 simple   2019.10.4

from PyQt5.QtWidgets import QLineEdit, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer

app = None # for ipython
app = QApplication([]) #★★★

import time
import os 

timer=Qtimer()
timer.setInterval(100) #1초마다, 100일경우 0.1초
timer.timeout.connect(onTimeOut) #timeout 발생 할때마다  onTimeOut호출


def do_something():
    _path="/home/hyun/works"
    it=os.scandir(_path)
    for i in it:
        if i.is_file() :
            st=os.stat(_path +'/'+ i.name)
            #print(i.name, st.st_size)
            #_str = i.name #  + ":" + str(st.st_size)
            #self.listWidget.addItem(_str)
    pass

def onFirstButtonClicked():
    #while True:
    #    do_something()
    #    pass
    timer.start()
    print("fist Clicked")
    
    
def onSecondButtonClicked():    
    print("second Clicked")
    
        
def setupUI(window):    
    layout = QVBoxLayout()
    button1 = QPushButton('QPushButton1')    
    button2 = QPushButton('QPushButton2')    
    button1.clicked.connect(onFirstButtonClicked) #only Qt's signal can be connected !!!
    button2.clicked.connect(onSecondButtonClicked) 
    layout.addWidget(QLabel('Hello World!'))
    layout.addWidget(button1)
    layout.addWidget(button2)
    window.setLayout(layout)
    return

w = QWidget()
setupUI(w)
w.show()
app.exec_() # loop
 