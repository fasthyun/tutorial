# -*- coding: utf-8 -*-
# 초급 과정 LAB1 (수정5)   2019.10.10, 2021,8.9

# python2인 경우 다음을 코드 맨위에 추가하여 사용한다. 
from __future__ import print_function  # python3.0처럼 print()함수 동작 ★★★

# 목표:
# 1. list, int , float 데이타 타입 
# 2. range() 사용법   
# 3. list  slice 사용하기 
# 4. list를 이용한 반복문 사용, while 반복문 사용 
# 5.  1부터 10000까지 합을 구하는 함수 만들기 
# 6. dict 개념, 사용법

# ipython에서 다음을 실행해 봅니다. 
a=[2,3,4,5,7]   #이건 리스트입니다.
len(a)  	  # len() 내장함수는 a의 현재 크기를 알려줍니다. ★★
print("a=",a)    # a값을 출력해줍니다. 
#문제: type(a) 결과는 뭘까요? ★★★★ 
#답:

i=10  
#문제:  type(i) ?   
#답: 

f=2.5 
#문제: type(f) ?
#답:

print("i=",i," f=",f)

# ipython에서 다음을 실행해 봅니다.
list(range(5))    # 이건 range()함수 입니다. 편하게 리스트를 만들어 줍니다. ★★★★

range(10)
range(2,10)  # 인자가 2개 , 결과는?
range(3,10)
range(0,10,2)  # 인자가 3개 , 결과는?

b=range(5)
#문제 : type(b) 결과는 ?  ★★★
#답:

print(a) # 현재 a리스트 내용
#문제  len(a) 결과는?  답 :

a.pop()  # 리턴값으로 하나 빼줍니다.  ★★★
a.pop()  # 하나 더 빼줍니다. 
#문제 : len(a) 몇개 남았나요?  답:
a.append(9)  # 결과는?
a.pop(0) # index값을 넣을 수도 있습니다.  결과는?
len(a)  # 결과는?

#결론: append(), pop()을 사용해서 list를 스택처럼 사용가능합니다. ★★★★

#----- 리스트의 slice기능 ----
a=range(20)
a[0:3]  # slice 사용은 이렇게 합니다. 결과는? ★★★
b=a[5:7]  # 쪼개기가 가능합니다.
type(b)  # 결과는?  
a[3:] # 이렇게도 쓰입니다.
a[-1] # 이건뭘까요?

#----- 연산자------
_sum = 1 + 5
mult = 6 * 3
result = ( 1 + 5 )*3

#----- 반복문 -----  
# 다음을  test.py 작성 후 실행 합니다 결과값은 ? 
a_list=[4,3,6,7] 

for i in  a_list  :  #for를 사용한 반복문
    print(i)

for i in [0,1,2,3] : # 이렇게도 가능~
    print(i)

for i,val in enumerate(a_list): #인덱스도 출력가능 ★★★
    print(i,val)

# C언어의 break와 continue도 있습니다.

#---- -비교문 ----
I=32
if I > 0 :
    print("True")
else: 
    print("False")

if type(I) == int : #파이써는 이런게 됩니다.
    print(" I is  int !!")
else :
    print(" I is Not int !!")
    
    
# while 이용한 반복문, 다음  출력 값을 예상해보시오!!!  ★★★
k=5
while k > 0 :
    print("k=",k)
    k = k -1
print(" out of loop k=",k)

# 다음 함수 작성해서 실행하기 
def my_func(b):
    if type(b) == int :
        print("type(b) is int !",b)
    else:
        print("type(b) is Not int !")
    return  # 없어도  가능함!

my_func(4) #함수 호출은 이렇게 합니다.

#문제1  ♨★★
# 1부터 1000까지 덧셈 가능한 코드 작성
#힌트: for문, range() 함수 사용하기! 
# 감독관 확인 꼭 받기 !!

#문제2  ♨♨★★
# 1부터  정수x  까지 덧셈가능한 함수 작성하기 

#문제3  ♨♨♨★★★
# while 문을 이용하여 2번문제 해결하기( C언어 스타일)

#----------------------------
# ipython에서 다음을 실행해 봅니다. 
a=[] #이건 list 
d={} #이건 dictionary 입니다.

a.append(1)
a.append(2)
#문제: 리스트 a 내용은 어떻게 되었을까요?

d['a']=32    # key 'a' , value 32 
d['b']=64
print(d)  # d 내용을 봅니다

d['hyun']="male"
d['joe']="female"

print(d)
print(d['hyun'])  # 이렇게 key를 이용해서 value를 불러옵니다.
print(d.keys()) # d의 모든 key를 알려줍니다.