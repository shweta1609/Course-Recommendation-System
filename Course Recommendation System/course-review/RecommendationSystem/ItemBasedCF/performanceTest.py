import numpy as np
#from userBasedCFAlgs import *
from itemBasedCFAlgs import *
from myUtil_i import *
### a simple test, with given userid in memory, return
def simpleTest():
    if not ('ratings' in locals()):
        courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL()
    user1 = '4'
    k=3
    #print(ratings)
    # for rat in ratings:
    #     print(len(ratings[rat]))


    # print(ratings[user1])
    pb,v=NewUserPrediction(ratings[user1],k,ratings,courseIDMap,similarity,returnType="more")
    print(pb)
    # pb,v=NewUserPrediction(ratings[user1],k,ratings,courseIDMap,similarity_cosine,returnType="more")
    # print(pb)
    # pb,v=NewUserPrediction(ratings[user1],k,ratings,courseIDMap,similarity_jaccard,returnType="more")
    # print(pb)
    # pb,v=NewUserPrediction(ratings[user1],k,ratings,courseIDMap,similarity_cosine,returnType="more")
    # print(pb)
    #print(ratings)
    #print(pall)

def simpleTest_itemBasedCF():
    if not ('ratings' in locals()):
        courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL()
    if not ('linesList' in locals()):
        linesList,courseIDMap,userIDMapInv=loadDataPKL_itemBasedCF()
    user1 = '418'
    k=1
    retN=4
    #pre=NewUserPrediction_itemBasedCF(ratings[user1],k,retN,courseIDMap,linesList)

    rat=ratings[user1]
    rat={'CS-6300': '3', 'CS-6400': '3', 'CS-6440': '3'}
    #rat={'CS-6262': '5'}
    pre=NewUserPrediction_itemBasedCF(rat,k,retN,courseIDMap)
    print(rat)
    print(pre)

def oneFoldTest(testdata,traindata):
    if not ('ratings' in locals()):
        courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL()
    # print(testdata)
    # print('---')
    # print(traindata)
    testdataModified={}
    testdataRowRemoved={}
    for d in testdata:
        l=list(testdata[d])
        length=len(testdata[d])
        rnum=np.random.randint(0,length)
        testdataRowRemoved[d]={l[rnum]:testdata[d][l[rnum]]}
        testdataModified[d]=testdata[d].copy()
        del testdataModified[d][l[rnum]]
    # print(testdata)
    # print('---')
    # print(testdataModified)
    # print('---')
    # print(testdataRowRemoved)
    # print('---')
    k=4
    count=0
    #for d in testdataModified:
    for d in testdataModified:
        #pb,pall=NewUserPrediction(testdataModified[d],k,traindata,courseIDMap,similarity_jaccard)
        pb,verbose=NewUserPrediction(testdataModified[d],k,traindata,courseIDMap,similarity,returnType="more")
        #pb,verbose=NewUserPrediction(testdataModified[d],k,traindata,courseIDMap,similarity,returnType="more")
        fullname={}
        # for p in pb:
        #     print(p,courseFullName[p])
        # for p in testdata[d]:
        #     print(p,courseFullName[p])

        # print("recommended: ",pb)
        # print("removed: ",testdataRowRemoved[d])
        # print("remained: ",testdataModified[d])
        #print("take", testdata[d])
        #print('---')
        # print(pb[0])
        #print(list(testdataRowRemoved[d].keys())[0])
        if verbose=="more" or verbose=="rand":
            for course in pb:
                if course == list(testdataRowRemoved[d].keys())[0]:
                    count+=1
        else:
            if pb[0] == list(testdataRowRemoved[d].keys())[0]:
                count+=1
           #print("match!")


    # print(count)
    # print(count/len(testdataModified))
    # print('---')
    return count/len(testdataModified)
    pass

def oneFoldTest_itemBasedCF(testdata,traindata):
    testdataModified={}
    testdataRowRemoved={}
    for d in testdata:
        l=list(testdata[d])
        length=len(testdata[d])
        rnum=np.random.randint(0,length)
        testdataRowRemoved[d]={l[rnum]:testdata[d][l[rnum]]}
        testdataModified[d]=testdata[d].copy()
        del testdataModified[d][l[rnum]]
    # print(testdata)
    # print('---')
    # print(testdataModified)
    # print('---')
    # print(testdataRowRemoved)
    # print('---')
    linesList,courseIDMap,userIDMapInv=loadDataPKL_itemBasedCF()
    linesList=[]
    for d in traindata:
        for item in traindata[d]:
            linesList.append([d,traindata[d][item],item])
    print(linesList)
    k=2
    retN=4
    count=0
    for d in testdataModified:
        pre=NewUserPrediction_itemBasedCF(testdataModified[d],k,retN,courseIDMap,linesList)
        print("recommended: ",pre)
        print("removed: ",testdataRowRemoved[d])
        print("remained: ",testdataModified[d])
        print('---')
        for course in pre:
            if course == list(testdataRowRemoved[d].keys())[0]:
                count+=1

    return count/len(testdataModified)

def kFoldtest(totalFold):
    if not ('ratings' in locals()):
        courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL()
    sumAcc=0
    for i in range(totalFold):
        test,train=splitRatingsKFold(ratings,totalFold,i+1)
        sumAcc+=oneFoldTest(test,train)
    # print("---")
    # print(sumAcc/totalFold)
    return(sumAcc/totalFold)
    # test,train=splitRatingsKFold(ratings,10,9)
    # oneFoldTest(test,train)

def kFoldtest_itemBasedCF(totalFold):
    if not ('ratings' in locals()):
        courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL()
    sumAcc=0
    for i in range(totalFold):
        test,train=splitRatingsKFold(ratings,totalFold,i+1)
        sumAcc+=oneFoldTest_itemBasedCF(test,train)
    # print("---")
    # print(sumAcc/totalFold)
    return(sumAcc/totalFold)
    # test,train=splitRatingsKFold(ratings,10,9)
    # oneFoldTest(test,train)

def RecallRate(itrNum=10,algs="userBasedCF"):
    if algs=="userBasedCF":
        sum=0
        for i in range(itrNum):
            num=kFoldtest(10)
            print(i,num)
            sum+=num
        print(sum/itrNum)
    else:
        sum=0
        for i in range(itrNum):
            num=kFoldtest_itemBasedCF(10)
            print(i,num)
            sum+=num
        print(sum/itrNum)
