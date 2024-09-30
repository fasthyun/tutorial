# -*- coding: utf-8 -*-
#PyQt5-LAB3 과정 (수정3)  2019.9.11

# 소스 위치 8.48.65.142 /home/sdr/SECLAB/tutor/
# 목표:   Qt Paint시스템 이해 
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
        self.setMinimumHeight(40) # hint 
        self.rect1= QRect(0,0,15,12) #x,y,width,height
        self.rect2= QRect(0,0,0,0)
        self.show() #
    
    def paintEvent(self, event):
        """ paintEvent()호출 되는 경우? assist 참조   """
        print("paintEvent1", event.rect())  # QRect객체 !!!
        p=QPainter() #Qpainter는 오직 paintEvent에서만 사용!!!
        p.begin(self)
        p.setPen(QColor(168,34,3)) #RGB
        #p.setFont(Qfont('Decorative',10))
        p.drawText(event.rect(), Qt.AlignCenter, self.text)
        p.setPen(QColor(50,100,50))  # 컬러 지정
        p.drawRect(self.rect1) # 사각형1 그리기 
        p.drawRect(self.rect2) # 사각형2 그리기 
        p.drawPoint(5,20)  # 점 그리기 
        p.end()    
    
mw=MyWidget()
def onRepaintClicked():
    print("repaint clicked!!!")    
    if mw.rect2.width() == 0:
        mw.rect2=QRect(20,20,15,12) #x,y,width,height
    else:
        mw.rect2=QRect(0,0,0,0) #x,y,width,height
    mw.update() # paintEvent() will be called 
    
def setupUI(window):    
    buttonRepaint=QPushButton('Repaint!')
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

#실습1 :  실행 후  repaint버튼을 누르면  사각형2가 그려지고 다시 누르면 없어진다.
#실습2 :  실행 후  윈도우 사이즈크기를  변경하면  paintEvent1이 출력된다.

#문제1:  onRepaintClicked()함수에서  mw.update() 주석처리하면,  결과는?
#힌트: 문제 3 
#답: 

#문제1:   MyWidget 크기를  (150, 80) 으로 바꾸오! ♨
#힌트:   assist에서 QWidget 메소드 참조 

#문제2:   MyWidget의 크기가 변할때  사각형1의 크기도 비례해서 커지게 수정하시오  ♨♨ ★★★
#힌트:  event.rect() 

#문제3:  MyWidget의 paintEvent()함수가  호출되는 경우는 어떤 경우에  발생하는가요? ♨♨ ♨♨ ★★★★
#힌트:   assist참조 , 문제1번, 실습2
#답:

#문제4 :  Repaint 버튼을 누르면  랜덤 점을  30개 이상 그리기  ♨♨♨♨
#힌트:  random 함수 사용!