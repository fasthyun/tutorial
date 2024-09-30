# 초급 과정  LAB2 (수정3)  수정  2019.10.11
 
# 목표:  . str 타입,  예외,에러 처리  ,  파일 open() , bytearray() 타입 사용법,  enumerate
s="Hello? I am a python!"
type(s) #  결과는?  ★

s = s + " for programmers!" # 덧셈 기능도 있습니다! ★

#실습: str타입은 리스트 처럼  iterator기능이 있습니다.  ★★★
for c in s: 
    print(c)

# slice(쪼개기)도 가능 합니다.★★★★
print(s[0:4]) 

#이렇게도 사용할수 있습니다.★★
for i in range(len(s)): 
    print(s[i]) 

type(s[0]) # 결과는 C언어와 다릅니다. 뭘까요?★★★★★★

#실습: 문자열 타입은 다양한 메소드(함수)를 갖습니다.
s.replace("python","snake")  # 결과는?
s.find("python")  # 인덱스를 리턴합니다.
s.split(" ")  # 공백문자 기준으로 쪼개줍니다. 결과는? 


# 문제:   아래 함수 채워넣기.
# 특정 문자열을 검색해서 index값을 돌려주는 find함수 구현!(str의find기능을 구현)
#힌트: for, enemerate() 
def find(s,sub):  
    idx=-1 #채워넣기
    return idx

# 문제: 특정문자열을 replace하고 리턴하는 함수를 구현하시오
# 힌트:  find함수 사용 가능
def replace(s,sub1,sub2): 
      #채워넣기
   return new_s

#실습: 다음을 실행하면 예외가 발생한다.  놀람금지!
a=list(range(3))
while True:
    print(a.pop())

#실습:  예외 처리가 적용된 코드★★★★
a=range(3)
while True:       
    try :
        print(a.pop())
    except Exception as e:
        print ("Exception !!",e,", ErrorType=",type(e))
        break
      
#실습: 더 세분화된 예외처리 , 무엇이 출력되나?
a=range(3)
while True:       
    try :
        print(a.pop())
    except IndexError:
        #print ("IndexError !!")
        print ("end of a !!")
        break
    except Exception as e:
        print ("Exception !!",e, "ErrorType=",type(e))    
        break 

#실습: 파일 쓰기, 실행 후  텍스트에디터로 꼭  확인 ! ★★★★★
f = open("test_write.txt","w")   # 파일 쓰기
f.write("python1 ")
f.write("python2\n python3\n")
f.write("python4\n")
f.close()
#문제 :  python100.txt파일에  1행부터 100행까지   python1 ~ python100을  손으로 작성 하시오  ★★★★
#답:  확인받을 것

#실습:  다음처럼 텍스트 파일을 read합니다. ipython에서 실행가능
f = open("test1_open.txt","r")   # 바이너리 파일은  반드시 "rb" 
data = f.read() # 파일 전체 읽기
f.close()  # 파일 닫기

type(data)  # 결과는?  ★★★★
data[0:19]  # 결과는? 
data[11:14] # 결과는? 

for i in data[11:19] :  # slice를 이렇게 사용가능~
    print("i=",i)

for i,k in enumerate(data[11:19]): #enumerate사용은 이렇게 ★★★
    print("i=",i, ",k=",k)

# file read()함수의 리턴값은 str타입이라서,   C언어 처럼 byte로 다루길 원한다면  
# bytearray()타입으로   바꾸면 된다. ★★★★
ba=bytearray(data.encode())  
type(ba[0]) # 결과는 C언어와 다릅니다. 뭘까요? ★★★
ba[0] # 결과는?
ba[1] # 결과는?

#문제 4:  산술연산(x,+)계산기 만들기 (곱은 x로 하기)   [예] 128x32+64
#힌트 : 입력함수는 input()사용

#문제 5:  다음 폴더의 파일들에서  확장자가 txt인 파일 골라서 출력하기.  C:/windows/
#힌트:  os.walk() 또는...

#LAB2 end
