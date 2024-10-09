# -*- coding: utf-8 -*-

# numpy-signal-LAB1 (수정5)  2020.5. 6,  2021.08.11

# Required :  Tutorial-python-numpy.py 

#---
#실습1:  math.sin과  numpy.sin 차이점  보기
import math
import numpy as np

#print(math.pi)
#print(np.pi)
#print(np.pi==math.pi) #결과는?

# 다음은  0, 90, 180, 270, 360도  sine값을 출력하는 코드입니다.
x0 = 2*math.pi*0.0/4  #0도
x1 = 2*math.pi*1.0/4  #90도
x2 = 2*math.pi*2.0/4  #180도
x3 = 2*math.pi*3.0/4  #270도
x4 = 2*math.pi*4.0/4  #360도
#---------- python's math ---------------------
y0 = math.sin(x0)
y1 = math.sin(x1)
y2 = math.sin(x2)
y3 = math.sin(x3)
y4 = math.sin(x4)
print("python ===> ",y0,y1,y2,y3,y4) #




# -------- 여기서부터는 numpy --------------------
x=[x0,x1,x2,x3,x4]
y=np.sin(x)
print("numpy ===> ", y)

#다음은 linspace()함수를 사용해서  위와  같이  출력하는 코드입니다. ★★★★
x = np.linspace(0, 2*math.pi, 4+1) 
y=np.sin(x)
print("linspace ===> ",y)


#생각1: linspace() 함수의 역할은? math.sin()와 numpy.sin() 중 어떤게 더 편리한가요?

#문제1:  1주기 사인파 만들고  plot하기  (샘플 갯수는 200개, math.sin이용)
#답:  감독관에게  꼭 확인  받기 !!

#문제2: 문제1을  numpy.sin(벡터.배열방식), linspace()사용 하여 구현하기 
#답:  감독관에게  꼭 확인  받기 !!

#end...