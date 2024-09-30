# -*- coding: utf-8 -*-
# LAB3 (수정3)  2019.10.11
  
# 목표: 
#    1.  파이썬 class 
#  2. Queue , time , sleep(), os, random

# 파이썬 class 사용하기
class MyPoint():
    def __init__(self): #생성시 자동 실행되는 초기화 함수입니다. 
        self.value=0  # 클래스 내부 변수는 self를 사용합니다 ★★★

    def incVal(self):
        self.value +=1
        
    def getVal(self):
        return self.value

    def setVal(self,new_val):
        self.value=new_val              

mp=MyPoint() # MyPoint를 사용하기위해 객체 생성을 합니다.
mp.getVal()  # 현재 값을 봅니다. 
mp.incVal()  # incVal()함수를 호출(실행)합니다. 
mp.getVal()  # 현재 값은? 

#문제1. mp의 타입은?   힌트: type(mp) 
#답: 

# queue는 thread safe를 지원하기때문에... 쓰레드에서 너무 너무 많이 사용합니다.
# 다음을  꼭  ipython 창에서 실행합니다. !
import queue  # python2에서는  Queue 입니다.
q=queue.Queue()
q.put(1)  #값을 집어 넣습니다.
q.put(2)  
q.put(3)  

q.get() # 값을 꺼냅니다. 뭘까요 ?
q.get() # 그 다음은?
q.get() # 그 다음은?
q.get() # 주의 ★★★★★★

#q.get_nowait() # 파이썬 도움말 꼭 읽기!!! ★★★★

#time() 함수 사용법 배우기
import time #표준 time 모듈을 임포트합니다.
#다음을  꼭  ipython 창에서 실행합니다. !
time.time()  #time모듈의 time()함수 호출
time.time()  #또 호출
time.time()  #또또 호출 ,  감이 오나요? 
#문제: time()함수는 대체 무엇을 출력하는 건가요? 
#답:

# 문제2:  다음 코드에서 dt 목적은 뭘까요 ?
#답: 
st=time.time() # start_time
_sum=0
for i in range(10000000):
    _sum+=i
print("sum=",_sum)

dt= time.time() - st  #delta_time: 
print("dt=",dt)


#random 함수 실습:  C언어에서는  random함수 사용이 까다롭지만, 파이썬은 쉽습니다.
import random
random.randint(0,10)  # 0부터 10까지 숫자중에 랜덤하게 리턴~
#문제 : 리턴값은 ? 

a=list(range(20))
random.shuffle(a) #return값 없음 
#문제 : a의 값은?

#문제 :  로또 번호 생성기 를  만드세요 !  조건 6개 번호 1~45 , randint 사용
#평가:  확인 필요!!!

#문제: 위 [로또생성기] 문제를 shuffle()을 사용해서  만들어 보기!
#평가:  확인 필요!!!

# LAB3 끝!
