# -*- coding: utf-8 -*- 
#PyQt5-LAB1 과정 (수정3)   2019.10.4

# 목표: . QApplication, QWidget, QLabel, QVBoxLayout 사용법

#1번 실습: 다음을 실행!
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

def setupUI(window):
    layout = QVBoxLayout()
    label = QLabel('Hello World!')
    layout.addWidget(label)
    window.setLayout(layout)
    return

app = None # for ipython
app = QApplication([])
w = QWidget()
setupUI(w)
w.show()
app.exec_() # loop

#2번실습 :  반응없는 QPushButton !
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

def setupUI(window):
    layout = QVBoxLayout()
    layout.addWidget(QLabel('Hello World!'))
    layout.addWidget(QPushButton('QPushButton'))
    window.setLayout(layout)
    return

app = None # for ipython
app = QApplication([])
w = QWidget()
setupUI(w)
w.show()
app.exec_() # loop

#문제: 2번 실습에서 QVBoxLayout을 QHBoxLayout으로 바꾸면 어떻게 변하나? ★
#답: 

#4번실습 connect를 이용한 clicked 이벤트처리 
from PyQt5.QtWidgets import QLineEdit, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

app = None # for ipython
app = QApplication([]) #★★★

lineedit= QLineEdit("python") # 전역변수로 ★★★★★

def onFirstButtonClicked():
    global lineedit
    print("fist Clicked")
    print("lineedit.text()=",lineedit.text())     
    
def onSecondButtonClicked():    
    global lineedit
    lineedit.setText("second clicked")
        
def setupUI(window):    
    layout = QVBoxLayout()
    button1 = QPushButton('QPushButton!')    
    button1.clicked.connect(onFirstButtonClicked) #only Qt's signal can be connected !!!
    button2.clicked.connect(onSecondButtonClicked) 
    layout.addWidget(QLabel('Hello World!'))
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(lineedit)
    window.setLayout(layout)
    return

w = QWidget()
setupUI(w)
w.show()
app.exec_() # loop
 
#문제5  ♨♨♨ ★★
#원금, 이율, 기간(년)을 입력 받고(QLineEdit), 최종 돌려받는 이자+원금 계산을 출력하기
#조건 : 입력 출력을  QLable또는 QLineEdit 사용

#end...
