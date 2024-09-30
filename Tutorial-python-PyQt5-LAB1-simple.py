# -*- coding: utf-8 -*- 
#PyQt5-LAB1 simple   2019.10.4

from PyQt5.QtWidgets import QLineEdit, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

app = None # for ipython
app = QApplication([]) #★★★

def onFirstButtonClicked():    
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
 