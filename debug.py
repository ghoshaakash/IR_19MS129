import csv
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
stemmer = PorterStemmer()

class film:
    def __init__(self,year,name,origin,director,cast,genre,url,plot):
        self.year=year
        self.name=name
        self.origin=origin
        self.director=director
        self.cast=cast
        self.genre=genre
        self.url=url
        self.plot=plot

def Bin_Serch(arr, key):
    first = 0
    last = len(arr) - 1
    while first <= last:
 
        mid = (last + first) // 2
        if arr[mid] < key:
            first = mid + 1
        elif arr[mid] > key:
            last = mid - 1
        else:
            return mid
    return -1
        
def Sort_Insert(arr,key):
    i = 0
    while i<len(arr):
        if arr[i]>key:
            break
        i=i+1
    arr.insert(i,key)
    return arr


FilmArr=[]
TokArr=[]
WordList=[]
with open("file.csv","r",encoding='utf-8') as file:
    reader=csv.reader(file)
    for line in reader:
        filmOb=film(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
        tok=[]
        tok=tok+word_tokenize(filmOb.plot)
        l=len(tok)
        i=0
        while(i<l):
            tok[i]=stemmer.stem(tok[i].lower())
            if (Bin_Serch(WordList,tok[i])==-1):
                WordList=Sort_Insert(WordList,tok[i])
            i=i+1
        tok.sort()
        TokArr.append(tok)
        FilmArr.append(filmOb)
        
inMAt=[[0]*len(WordList)for _ in range(len(TokArr))]
i=0
while(i<len(TokArr)):
    lastTok=""
    lastIndex=-1
    for j in TokArr[i]:
        if j==lastTok:
            inMAt[i][lastIndex]=inMAt[i][lastIndex]+1
        else:
            lastTok=j
            lastIndex=Bin_Serch(WordList,j)
            inMAt[i][lastIndex]=inMAt[i][lastIndex]+1
    i=i+1
    
invertedIndex=[]
i=0
while(i<len(WordList)):
    imCol=[]
    j=0
    while(j<len(FilmArr)):
        if inMAt[j][i]!=0:
            imCol.append(j)
        j=j+1
    i=i+1
    invertedIndex.append(imCol)

def arrAnd(arr1,arr2):
    arr=[]
    for i in arr1:
        if i in arr2:
            arr.append(i)
    return arr

def arrOr(arr1,arr2):
    arr=[]
    for i in arr1:
        arr.append(i)
    for i in arr2:
        flag=1
        for j in arr1:
            if i==j:
                flag=0
        if flag:
            arr.append(i)
    return arr

def arrAndNot(arr1,arr2):
    arr=[]
    for i in arr1:
        if i not in arr2:
            arr.append(i)
    return arr


def query(arr):
    try:
        i=0
        stack=[]
        while(i<len(arr)):
            
            if arr[i]==")":
                if stack[-2]=="AND":
                    temp=arrAnd(stack[-1],stack[-3])
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.append(temp)
                elif stack[-2]=="OR":
                    temp=arrOr(stack[-1],stack[-3])
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.append(temp)
                else:
                    temp=arrAndNot(stack[-1],stack[-3])
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    stack.append(temp)
            else:
                stack.append(arr[i])
            i=i+1
        return stack[0]
    except:
        print("Error in query processing")
        return -1
        
while(1):
    str=input("Enter query. Query words are to be given in small case and Query relation operators are to be given in upper case. Query realtion operators are considered to be binary realations. Enter a digit to quit.\n")
    str=str+" "
    if(str.isnumeric()):
        break
    tok=[]
    tempStr=""
    i=0
    while(i<len(str)):
        if str[i]=="(":
            tok.append(tempStr)
            tok.append("(")
            tempStr=""
            i=i+1
        elif str[i]==")":
            tok.append(tempStr)
            tok.append(")")
            tempStr=""
            i=i+1
        elif(str[i]==" "):
            tok.append(tempStr)
            tempStr=""
            i=i+1
        else:
            tempStr="".join([tempStr,str[i]])
            i=i+1
    for i in tok:
        if(len(i)==0):
            tok.remove(i)
    i=0
    while(i<len(tok)):
        if (tok[i]!="AND")and(tok[i]!="OR")and(tok[i]!="ANDNOT")and(tok[i]!="(")and(tok[i]!=")"):
            tok[i]=stemmer.stem(tok[i].lower())
            r=Bin_Serch(WordList,tok[i])
            if(r==-1):
                tok[i]=[]
            else:
                tok[i]=invertedIndex[r]
        i=i+1
                
    arr=query(tok)
    if(arr!=-1):
        print("Match list is:")
        l=len(arr)
        i=0
        while(i<l):
            print(FilmArr[arr[i]].name)
            i=i+1