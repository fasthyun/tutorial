# -*- coding: utf-8 -*- 
#  PyQt-LAB2 과정 (수정3)  2019.11.2

# 목표:  QTimer 
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout,QPushButton
from PyQt5.QtCore import QTimer

app = None #
app = QApplication([]) #first of all Q*

time=0
timer=QTimer() 

def onButtonClicked():
    global timer
    global onTimeout
    print("clicked!!!")
    #if timer.isActive() == False : 
    #    timer.start() #시작 
    
def onTimeOut():
    global time
    time+=1
    print(time)

def setupUI(window):    
    layout = QVBoxLayout()
    button=QPushButton('start')
    button.clicked.connect(onButtonClicked) #only Qt's SIGNAL can be connected!!!
    layout = QVBoxLayout()
    layout.addWidget(QLabel('Timer Example'))
    layout.addWidget(button)
    window.setLayout(layout)
    return

timer.setInterval(1000) #1초마다, 100일경우 0.1초
timer.timeout.connect(onTimeOut) #timeout 발생 할때마다  onTimeOut호출

w=QWidget()
setupUI(w)
w.show()
app.exec_() #loop

#실습1: 위 코드를 실행해서 한번 누르고 나면  1초마다 onTimeout() 호출 된다.

#문제1: Qtimer를 정지할 수있는 정지 버튼(QPushButton) 추가 하기  
#힌트: QTime.stop() 

#문제2:   시, 분 , 초  전시하는 시계 만들기  ★★ 
# datetime.datetime.now() 또는 QDatetime

#문제3: 초단위 타이머 만들기, 시간입력(예:5초), 스타트버튼, 남은시간 (초) 출력 (QLabel) ♨★

#문제4: 밀로초 타이머 만들기 ♨♨♨♨★★★
#조건: setInterval(30) # 30ms로 만들것 
#힌트: 파이썬의 time.time() 또는 QDateTime.currentMSecsSinceEpoch () 사용

#문제5: 위 문제에서  Start, Stop을 하나 버튼으로 합치기 
# start 버튼을 누르면  stop으로 변신 .....

#문제6:  실습1코드에서  timer.isActive() == False 가 없으면 어떤 문제가 발생하는가 ?  ♨♨♨♨♨

#LAB2 끝

