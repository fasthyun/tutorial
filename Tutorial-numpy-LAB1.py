# -*- coding: utf-8 -*- 

# numpy-LAB (수정1)  2019.10.30

#목표:  numpy 배열 (array) 이해 
import numpy as np  

a   = [1,2,3,4,3,2,3]  #파이썬 list()
b   = [2,4,3,2,1,4,5]
c   = [9,7,8]

na  = np.array(a)  # numpy array
nb  = np.array(b)  
nc  = np.array(c)

#문제 : type(na) ? ★★

#문제 :  a*2  결과는?

#문제 :  na*2  결과는?

#문제:  na - nb 결과는 ? ★★★

#문제: na.min(), na.max()  결과는? 

#문제 :  numpy.array에는 argmax()함수가 있다.   na.argmax() 결과는?     ★★★★★★
# numpy.argmin()

#문제:  na.sum()★★★★★★ 

#문제:  na > 2 결과는? ★★★★

#문제 :  numpy array빠르게 만들기  , 다음 결과는?
nd = np.array(range(10)) 
ne = np.arange(10)   # nd와 같은 결과당 ! ★★
nf = np.zeros(10) #★★
ng = np.ones(10)  #★★
nh = np.linspace(0,5,10) # ★★★★★★★

#실습: append 하기 ★
nc=np.append(na,nb) 

# ndarray의 중요 속성들 
na.shape  # 배열 모양 
na.ndim   # 전체원소수  ?????
na.dtype  # 원소의 데이타 타입: int ,float , byte 등등  ★★★

#실습:  dtype을 이용하여  int, float 배열 생성
n_i = np.arange(10,dtype=np.int32) 
n_f = np.arange(10,dtype=np.float32) 

# matplotlib실습1 : y값만으로 plotting하기  ★★★★★★
import matplotlib.pyplot as plt
plt.plot(na) 
plt.grid()
plt.title("Plot na")
plt.show() 

# matplotlib실습2 : x,y값으로 plotting하기 
nx=np.arange(len(nb))
plt.plot(nx,nb)
plt.grid()
plt.title("Plot nb")
plt.show()

# numpy 유용한 함수들
np.pi # 파이값  
np.abs(-5) #
np.round(5.1)
np.min(nb)
np.max(nb)
np.ceil(nb)
np.floor(nb)
np .sin(nb)

'''
#실습 :   반복문 
for i in n_i: #이런게 된다.
    print(i)

#----------- Advanced Questions -----------
#  덧셈 성능 테스트(benchmark) 작성중
#   
# end...
'''