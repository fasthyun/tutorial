# -*- coding: utf-8 -*-
#PyQt5-LAB7 과정 (수정1)  2025.6.6

# 소스 위치 8.48.65.142 /home/sdr/SECLAB/tutor/
# 목표:   Qt Paint시스템 이해 
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor 
from PyQt5.QtCore import Qt, QRect, QTimer 

import numpy as np
import time

app = None #for ipython 
app = QApplication([]) #first of all Q*

class Brick:
    def __init__(self,_size, _x, _y):
        self.x=_x
        self.y=_y
        self.size=_size
        self.rect = QRect(0,0,_size,_size)        
        self.color= QColor(168,34,3)
        pass
    def draw(self,p): 
        self.rect.moveTo(self.x*self.size, self.y*self.size)  
        p.fillRect(self.rect,self.color)
        pass

#1. QPushButton's parent?
class MyWidget(QWidget): #class for painting
    def __init__(self):
        super().__init__() #QWidget.init
        self.text = "MyWidget"
        self.brick_size=16
        self.brick_width_n=32
        self.brick_height_n=32
        self.bricks=[]
        
        self.prev_epoch=time.time()
        self.drop_time = 0
        self.frame_per_seconds = 0
        self.frame_time = 0
        self.frame_count = 0
        #self.setGeometry(300, 300, 280, 170) # useless by Qlayout !!
        self.setMinimumHeight(self.brick_height_n*self.brick_size) # hint 
        self.setMinimumWidth(self.brick_width_n*self.brick_size) # hint 

        self.show() #
        for i in range(40):            
            x = np.random.randint(0,32)
            y = np.random.randint(0,32)
            brick = Brick(self.brick_size,x,y)
            self.bricks.append(brick)
            
    def process(self):
        _now = time.time()
        _dt = _now - self.prev_epoch
        self.prev_epoch = _now
        #print("dt=", _dt)
        
        self.drop_time += _dt
        self.frame_time += _dt
        
        if self.drop_time > 0.5 :
            #for blk in self.bricks:
            #    blk.y += 1
            self.drop_time =0
            
        if self.frame_time > 1.0 :
            self.frame_time=0
            self.frame_per_seconds = self.frame_count 
            self.frame_count=0
        
        self.update() # occurs paintEvent !! 
        pass
    
    def paintEvent(self, event):
        """ paintEvent()호출 되는 경우? assist 참조   """
        self.frame_count +=1         
        #print("paintEvent", event.rect())  # QRect객체 !!!
        _rect=event.rect()
        p=QPainter() #Qpainter는 오직 paintEvent에서만 사용!!!
        p.begin(self)
        p.setPen(QColor(168,34,3)) #RGB
        #p.setFont(Qfont('Decorative',10))
        _str = self.text + ", FPS=" + str(self.frame_per_seconds)
        p.drawText(event.rect(), Qt.AlignCenter, _str)
        p.setPen(QColor(50,100,50))  # 컬러 지정
        p.drawRect(0,0,_rect.width()-1,_rect.height()-1) # 사각형 그리기 
        for blk in self.bricks:
            blk.draw(p)
        #p.drawPoint(5,20)  # 점 그리기 
        p.end()    
    
    
mw=MyWidget()
    
def setupUI(_widget):    
    layout = QVBoxLayout()
    layout.addWidget(QLabel('Hello World!'))
    layout.addWidget(mw)
    _widget.setLayout(layout)
    return

timer=QTimer()
timer.setInterval(0)
timer.timeout.connect(mw.process)
timer.start()

w = QWidget()
setupUI(w)
w.show()
app.exec_() #loop
del timer
