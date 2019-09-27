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
    courseFullName=load(pathPre+"courseFullName.pkl")
    likeMap=load(pathPre+"likeMap.pkl")
    userIDMap=load(pathPre+"userIDMap.pkl")
    userIDMapInv=load(pathPre+"userIDMapInv.pkl")
    courseIDMap=load(pathPre+"courseIDMap.pkl")
    userRatings=load(pathPre+"userRatings.pkl")
    return courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,userRatings

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
