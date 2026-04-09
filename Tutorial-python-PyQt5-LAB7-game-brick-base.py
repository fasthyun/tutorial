# -*- coding: utf-8 -*-
#PyQt5-LAB7 과정 (수정1)  2025.6.6

# 소스 위치 8.48.65.142 /home/sdr/SECLAB/tutor/
# 목표:   Qt Paint시스템 이해 
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor , QFont
from PyQt5.QtCore import Qt, QRect, QTimer 

import numpy as np
import time

app = None #for ipython 
app = QApplication([]) #first of all Q*
label=QLabel('Hello World!')

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
    
class Brick_dong:
    def __init__(self,_size, _x, _y):
        self.x=_x
        self.y=_y
        self.size=_size
        self.rect = QRect(0,0,_size,_size)        
        self.color= QColor(0,255,0) #green
        pass
    def draw(self,p): 
        self.rect.moveTo(self.x*self.size, self.y*self.size)  
        p.fillRect(self.rect,self.color)
        pass
STATE_RUN = 1
STATE_DEMO = 2
STATE_INIT = 3
STATE_START = 4
STATE_GAMEOVER = 5

#1. QPushButton's parent?
class MyWidget(QWidget): #class for painting
    def __init__(self):
        super().__init__() #QWidget.init
        self.text = "MyWidget"
        self.brick_size=16
        self.brick_width_n=24
        self.brick_height_n=24
        self.bricks=[]
        self.brick_green=None
        self.prev_epoch=time.time()
        self.drop_time = 0.5
        self.drop_time_grow = 0
        self.frame_per_seconds = 0
        self.frame_time = 0
        self.frame_count = 0
        self.play_time=0
        self.play_level = 1
        self.state=STATE_DEMO #
        
        #self.setGeometry(300, 300, 280, 170) # useless by Qlayout !!
        self.setMinimumHeight(self.brick_height_n*self.brick_size) # hint 
        self.setMinimumWidth(self.brick_width_n*self.brick_size) # hint 
        #self.game_init() #
        #self.activateWindow()
        #self.setFocus()
        #self.show()
        
    def game_init(self):
        self.drop_time = 0.4
        self.play_time=0
        self.play_level = 1
        self.bricks=[]
        center_x = int(self.brick_width_n/2)
        self.brick_green = Brick_dong(16,center_x,self.brick_height_n-2)
        self.bricks.append(self.brick_green)
        
        for i in range(40):            
            x = np.random.randint(0,32)
            y = np.random.randint(0,32)
            brick = Brick(self.brick_size,x,y)
            self.bricks.append(brick)
    def check_collision(self):
        for b in self.bricks:
            if b == self.brick_green :
                continue
            if b.y == self.brick_green.y and b.x == self.brick_green.x :
                return True
                
        return False
    
    def process(self):
        _now = time.time()
        _dt = _now - self.prev_epoch
        self.prev_epoch = _now
        #print("dt=", _dt)
        
        self.drop_time_grow += _dt
        self.frame_time += _dt
        if self.state == STATE_DEMO:
            pass
        if self.state == STATE_RUN:    
            self.play_time += _dt
            if self.drop_time_grow > self.drop_time :
                for blk in self.bricks:
                    if type(blk) == Brick:
                        blk.y += 1
                self.drop_time_grow = 0
                
            if self.frame_time > 1.0 :
                self.frame_time=0
                self.frame_per_seconds = self.frame_count 
                self.frame_count=0
                
            if self.play_time > self.play_level*3 : 
                self.play_level += 1
                if self.drop_time > 0.15 :
                    self.drop_time -= 0.1 
                
        for b in self.bricks: # end of bricks ---> rebirth in top
            if b.y > 32 :
                b.y = 0
                b.x = np.random.randint(0,32)
        
        if self.check_collision() == True:
            self.state=STATE_GAMEOVER
        
        
        label.setText(f"play time : {self.play_time:.2f}")
        self.update() # occurs paintEvent !!
        pass
    
    def focusInEvent(self,e):
        print(e)
        
    def keyPressEvent(self, event):
        e=event
        if e.key() == Qt.Key_Escape:
           self.close()
        if self.state == STATE_RUN:
            if e.key() == Qt.Key_Right:
                if self.brick_green.x < (self.brick_width_n -1) : 
                    self.brick_green.x +=1
            if e.key() == Qt.Key_Left:
                if self.brick_green.x > 0: 
                    self.brick_green.x -=1            
        if self.state in [ STATE_DEMO, STATE_GAMEOVER] :
            if e.key() == Qt.Key_F5:
                self.game_init()
                self.state=STATE_RUN
        
        print(e)
           
    def paintEvent(self, event):
        """ paintEvent()호출 되는 경우? assist 참조   """
        self.frame_count += 1         
        #print("paintEvent", event.rect())  # QRect객체 !!!
        _rect=event.rect()
        p=QPainter() #Qpainter는 오직 paintEvent에서만 사용!!!
        p.begin(self)
        p.setPen(QColor(168,34,3)) #RGB
        _str = self.text + ", FPS=" + str(self.frame_per_seconds)
        
        p.setFont(QFont("Arial", 10))
        p.drawText(5,20,  _str)
        
        if self.state == STATE_GAMEOVER :            
            p.setPen(QColor(30,34,200)) #RGB
            p.setFont(QFont("Arial", 22 , QFont.Bold))
            p.drawText(event.rect(), Qt.AlignCenter, "GAME OVER")
  
        if self.state == STATE_DEMO :
            p.setPen(QColor(30,34,200)) #RGB 
            p.setFont(QFont("Arial", 20 , QFont.Bold))
            p.drawText(event.rect(), Qt.AlignCenter, "press F5 to start")
         
        p.setPen(QColor(50,100,50))  # 컬러 지정
        p.drawRect(0,0,_rect.width()-1,_rect.height()-1) # 사각형 그리기 
        
        for blk in self.bricks:
            blk.draw(p)
        #p.drawPoint(5,20)  # 점 그리기 
        p.end()    

    
mw=MyWidget()
    
def setupUI(_widget):    
    layout = QVBoxLayout()
    layout.addWidget(label)
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
mw.setFocus()
app.exec_() #loop
del timer
