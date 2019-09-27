#! /usr/bin/ python3
import pickle

def dump(filename,data):
    with open(filename,'wb') as f:
        pickle.dump(data,f,protocol=2)

def load(filename):
    with open(filename,'rb') as f:
        data=pickle.load(f)
    return data

def loadDataPKL(pathPre="dataPKL/"):
    difficultyMapInv={0:'Very Hard', 1:'Hard', 2:'Medium', 3:'Easy', 4:'Very Easy'}
    likeMapInv={0:'Strongly Disliked',1:'Disliked',2:'Neutral',3:'Liked',4:'Loved!'}
    loadMapInv={0:'very heavy', 1:'heavy', 2:'moderate', 3:'light', 4:'very light'}
    sentimentMapInv={0:'Very negative', 1:'Negative', 2:'Neutral', 3:'Positive', 4:'Very positive'}
    courseFullName=load(pathPre+"courseFullName.pkl")
    userIDMap=load(pathPre+"userIDMap.pkl")
    userIDMapInv=load(pathPre+"userIDMapInv.pkl")
    userIDMapMap=load(pathPre+"userIDMapMap.pkl")
    userIDMapMapInv=load(pathPre+"userIDMapMapInv.pkl")
    courseIDMap=load(pathPre+"courseIDMap.pkl")
    courseIDMapInv=load(pathPre+"courseIDMapInv.pkl")
    return courseFullName, userIDMap, userIDMapInv, userIDMapMap, userIDMapMapInv, courseIDMap, courseIDMapInv
    #return courseFullName, userIDMap, userIDMapInv, userIDMapMap, userIDMapMapInv, courseIDMap, courseIDMapInv, difficultyMapInv, likeMapInv, loadMapInv, sentimentMapInv

def loadDataPKL_itemBasedCF(pathPre="dataPKL/"):
    linesList=load(pathPre+"user2.pkl")
    courseIDMap=load(pathPre+"courseIDMap.pkl")
    userIDMapInv=load(pathPre+"userIDMapInv.pkl")
    return linesList,courseIDMap,userIDMapInv

def splitRatingsKFold(ratings,totalFold=10,thisFold=1):
    traindata={}
    testdata={}
    index=list(ratings)
    length=len(index)
    foldLength=(length//totalFold)

    start=(thisFold-1)*foldLength
    end=thisFold*foldLength

    foldRange=range(start,end)
    outRange1=range(0,start)
    outRange2=range(end,length)
    for i in range(length):
        if i in foldRange:
            testdata[index[i]]=ratings[index[i]]
        else:
            traindata[index[i]]=ratings[index[i]]
    return testdata,traindata

def vectorToCourseTokenList(v,c,courseNum):
    colNum=len(v)
    tookIndex=[]
    for i in range(courseNum):
        courseTookFlag=False
        for j in range(c):
            courseTookFlag=courseTookFlag or (v[c*i+j]!=0) # if all course attr is non zero, the this course took before
        if courseTookFlag:
            tookIndex.append(i)
    return tookIndex
