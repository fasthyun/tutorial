# -*- coding: utf-8 -*-
#PyQt5-LAB3-advanced 과정 (초안1)  2021.8.11(양대현)

# 소스 위치 8.48.65.142 /home/sdr/SECLAB/tutor/

# 목표: Qt 이벤트 처리 이해 ,  처리 설계 개념

# - 주어진 data(int16)파일의  버스트 개수를 구하는 프로그램 
# - QProgressBar를 이용, 처리 진행율 표시!
# - 버스트 개수를 구하기 힘들면 1보다 큰 개수를 구하라! 
# - 쓰레드 사용 금지!

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor 
from PyQt5.QtCore import Qt, QRect

app = None #for ipython 
app = QApplication([]) #first of all Q*

#1. QPushButton's parent?
class MyWidget(QWidget): #class for painting
    def __init__(self):
        super().__init__() #QWidget.init
        self.text = "MyWidget"
        #self.setGeometry(300, 300, 280, 170) # useless by Qlayout !!
        self.setMinimumHeight(200) # hint height
        self.setMinimumWidth(300) # hint width
        self.show()#
    
mw=MyWidget()
def onRepaintClicked():
    pass
    
def setupUI(window):    
    buttonRepaint=QPushButton('시작')
    buttonRepaint.clicked.connect(onRepaintClicked) #only Qt's slot can be connected!!!        
    layout = QVBoxLayout()
    layout.addWidget(QLabel('Hello World!'))
    layout.addWidget(buttonRepaint)
    layout.addWidget(mw)
    window.setLayout(layout)
    return
    
w = QWidget()
setupUI(w)
w.show()
app.exec_() #loop 