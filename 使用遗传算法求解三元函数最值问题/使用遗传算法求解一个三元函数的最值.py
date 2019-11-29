import random
import math
import time
personNum=1000 #种群数量
mutationProbability=0.9 #变异概率
iteration=50 #假设迭代50次即终止
length=30

def getAbsList(theList):
    for i in range(len(theList)):
        if theList[i]<0:
            theList[i]=theList[i]*(-1)
    return theList

# 功能：生成初始化种群
# 参数：personNum为种群数量，length为种群每个个体编码的位数
def initialPopulation(personNum=50,length=30):
    totalPopulation=[]
    while len(totalPopulation)!=personNum:
        person=[]
        for i in range(30):
            temp = random.uniform(-1, 1)  # 生成-1<=X<=1的数字
            if temp<0:
                person.append(0)
            else:
                person.append(1)
        theStr = ''
        for item in person:
            theStr += str(item)
        #print(theStr)
        if theStr not in totalPopulation:
            if evaluate(theStr)>0:
                totalPopulation.append(theStr)
        #print(len(totalPopulation))
    return totalPopulation


# 函数功能：将一个30位的编码转换为x,y的十进制解
def decode(onePerson,length=40):
    x = onePerson[0:15]
    y = onePerson[15:30]
    x = int(x, 2)
    y = int(y, 2)
    #print(x,y)
    if x < 16384:
        x = (x-16384) / 16384
    else:
        x = (x - 16384) / 16384

    if y < 16384:
        y = (y-16384) / 16384
    else:
        y = (y - 16384) / 16384

    return x,y


# 功能：计算x,y对应的函数值
# 参数：一个个体的编码
def evaluate(onePerson):
    x,y=decode(onePerson)
    result=x*math.sin(4*math.pi*x)-y*math.sin(4*math.pi*y+math.pi)+1
    return result

# 功能：获取一个父母进行交叉
# 输出：返回的是一个双亲在population的index
def getParents(evalList):
    temp = random.uniform(0, 1)
    #print(temp)
    portionList=[];theSum=0
    totalEval=sum(evalList)
    #print(totalEval)
    for eval in evalList:
        theSum+=eval/totalEval
        portionList.append(theSum)
    location=0
    while(temp>portionList[location]):
        location+=1
    #print('location=',location)
    return location


# 输入：两个person
# 输出：生成的子代person编码
def getCross(father,mother):
    theVisit=[]
    crossLocation=random.randint(0,29)
    theVisit.append(crossLocation)
    #print(crossLocation)
    child=''
    child += father[0:crossLocation]
    child += mother[crossLocation:30]
    while evaluate(child)<0:
        print("重新交叉")
        while crossLocation in theVisit and len(theVisit)<30:
            crossLocation = random.randint(0, 29)
            #print(crossLocation)
            child += father[0:crossLocation]
            child += mother[crossLocation:]
        theVisit.append(crossLocation)
        if len(theVisit)>=30:
            child=father
        #print(len(child))
    return child


# 功能：进行变异
def getVari(person):
    #print(person)
    temp = random.uniform(0, 1)
    if temp<mutationProbability:
        #print('变异')
        location=random.randint(0,29)
        #print(location)
        tempStr=person[0:location]
        tempStr+=str(1-int(person[location]))
        tempStr+=person[location+1:]
        if evaluate(tempStr)>evaluate(person):
            return tempStr
    return person


if __name__=='__main__':
    theScore=[]
    bestPerson=[]
    theBestEval=0

    for i in range(20): #设置跑多少轮，用来查看收敛性的
        population = initialPopulation(personNum, length)
        flag = 0
        timeStart=time.time()
        while flag!=iteration:
            print("第",flag+1,"代")
            evalList=[]
            tempPopulation=[]
            for person in population:
                evalList.append(evaluate(person))
            maxEval=max(evalList)
            print('maxEval=',maxEval)
            theIndex=evalList.index(maxEval)
            tempPopulation.append(population[theIndex]) #每次迭代时先将上一代最大的个体放到下一代种群中
            print("开始交叉")
            for i in range(personNum):
                #获得用于交叉的父母
                parentsFaIndex=getParents(evalList)
                parentsFa=population[parentsFaIndex]
                parentsMaIndex=getParents(evalList)
                parentsMa=population[parentsMaIndex]
                child=getCross(parentsFa,parentsMa)

                child=getVari(child)
                tempPopulation.append(child)
            population=tempPopulation
            flag+=1

            evalList = []
            for person in population:
                evalList.append(evaluate(person))
            maxEval=max(evalList)
            if theBestEval<maxEval:
                theBestEval=maxEval
            theIndex = evalList.index(maxEval)
            person = population[theIndex]
            if person not in bestPerson:
                bestPerson.append(person)
                theScore.append(1)
            else:
                theScore[bestPerson.index(person)] += 1
        print('duration=',time.time()-timeStart)

    print(theScore)
    print(bestPerson)
    theBestEvalList=[]
    for item in bestPerson:
        theBestEvalList.append(evaluate(item))
    print(theBestEvalList)
    print(theBestEval)
    print(max(theScore))

