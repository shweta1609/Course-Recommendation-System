import math
import sys
import pickle
import os.path as osp
from myUtil_i import *
from performanceTest import *




def getUserRatings(myList):
    # filename="dataPKl/coursesDict.pkl"
    # if osp.isfile(filename):
    #     data=load(filename)
    #     return data
    # else:
    #     tempDict={}
    #     for eachList in myList:
    #         course=eachList[course_name]
    #         user=eachList[userId]
    #         userRating=eachList[rating]
    #         if course in tempDict:
    #             tempDict[course][user]=float(userRating)
    #         else:
    #             tempDict[course]={}
    #             tempDict[course][user]=float(userRating)
    #     print("dump coursesDict")
    #     dump(filename,tempDict)
        # return tempDict
    tempDict={}
    for eachList in myList:
        course=eachList[course_name]
        user=eachList[userId]
        userRating=eachList[rating]
        if course in tempDict:
            tempDict[course][user]=float(userRating)
        else:
            tempDict[course]={}
            tempDict[course][user]=float(userRating)
    return tempDict

def getItemsList(myList):
    tempList=[]
    for eachList in myList:
        course=eachList[course_name]
        if course not in tempList:
            tempList.append(course)
    tempList.sort()
    return tempList

def getUnumratedcourses(user,mDict):
    tempDict={}
    tempDict[user]=[]
    userList=[]
    for eachcourse in mDict:
        if user not in mDict[eachcourse]:
            tempDict[user].append(eachcourse)
    tempDict[user].sort()
    return tempDict

def getUnratedcourses(user,iList,mDict):
    tempDict={}
    tempDict[user]=[]
    userList=[]
    for eachcourse in mDict:
        if user not in mDict[eachcourse]:
            tempDict[user].append(eachcourse)
    tempDict[user].sort()
    return tempDict

def getCommonUsers(dict1,dict2):
    tempList=[]
    for key in dict1:
        if key in dict2:
           tempList.append(key)
    return tempList

def getAvg(myList,myDict):
    total=0
    if len(myList)==0:
        return 0
    for user in myList:
        total+=myDict[user]

    mean=float(total)/float(len(myList))
    return mean


def mainDo(userName,n,k,linesList=None):
    global userId
    global rating
    global course_name
    userId=0
    rating=1
    course_name=2
    userName=int(userName)
    if linesList==None:
        linesList,courseIDMap,userIDMapInv=loadDataPKL_itemBasedCF("../ItemBasedCF/dataPKL/")
    else:
        trash,courseIDMap,userIDMapInv=loadDataPKL_itemBasedCF("../ItemBasedCF/dataPKL/")
    #print(userIDMapInv[418])
    #print(data)
#Create a Dictionary in the format -
#coursesDict{
#	course1:{
#		user1:Rating1,
#		user2:Rating2....}
#	course2:{
#		user1:Rating1,
#		user2:Rating2....}
    coursesDict=getUserRatings(linesList)
    #if Print==True:
    #    print coursesDict


    unratedcoursesDict={}
    itemsList=list(courseIDMap.keys()) #List of all the unique courses in the given .tsv
#Dictionary of all the unrated courses by a user(passed as argv)
#unratedcoursesDict={User:[course1,course2...]}
    unratedcoursesDict=getUnratedcourses(userName,itemsList,coursesDict)
    #print(unratedcoursesDict)
    #print(linesList[:10])

#Calculating the pearson correlation
    W={}
    for course in unratedcoursesDict[userName]:
        W[course]={}
    for urcourse in W:
        for course in coursesDict:
            if course!=urcourse:
                commonUsersList=getCommonUsers(coursesDict[urcourse],coursesDict[course]) #Get the list of co-rated users for unrated course, rated course pair
                avgURcourse=getAvg(commonUsersList,coursesDict[urcourse]) #Average rating of unrated course
                avgRcourse=getAvg(commonUsersList,coursesDict[course]) #Average rating of rated course
                Nr=Dr=term1=term2=0

#Nr=summation of [Ru,i - Avg(R)] * [Ru,j - Avg(R)]
#term1 = Square root of summation of [Ru,i - Avg(R)]^2
#term1 = Square root of summation of [Ru,j - Avg(R)]^2
#Dr=term1 * term2
#Pearson correlation= Nr/Dr
                for user in commonUsersList:
                    Nr+=(coursesDict[urcourse][user]-avgURcourse)* (coursesDict[course][user]-avgRcourse) #Nr=Numerator
                    term1+=(coursesDict[urcourse][user]-avgURcourse)**2
                    term2+=(coursesDict[course][user]-avgRcourse)**2
                term1=math.sqrt(term1)
                term2=math.sqrt(term2)
                Dr=term1*term2 #Dr=Denominator
                if Dr!=0:
                    val=Nr/Dr
                else:
                    val=0
                W[urcourse][course]=val
    #if Print==True:
     #   print "W"
    #print(W)

    newDict={}
    for urcourse in W:
        tempList=[]
        d=W[urcourse]
#Sort all the values in dictionary in descending order. If the values are same, then sort ther keys in alphabetical order
        tempList=[v[0] for v in sorted(d.items(), key=lambda kv:(-kv[1],kv[0]))]
        newDict[urcourse]=tempList
    #if Print==True:
    #print(newDict)


#Make prediction for courses with highest pearson correlation for the given user
    predictionDict={}
    for urcourse in newDict:
        Nr=Dr=0.00000
        m=n
        if len(newDict[urcourse]) < n:
            m=len(newDict[urcourse])
        i=0
        # print("---")
        # print(m)
        # print(urcourse)
        while i<m:
            rcourse=newDict[urcourse][i]
            #print(coursesDict[rcourse])
            if userName in coursesDict[rcourse]:
#Nr=Summation of Ru,n * Wi,n
#Dr=Summation of Wi,n
#Prediction for user u for item i = Nr/Dr
                Nr+=W[urcourse][rcourse]*coursesDict[rcourse][userName]
                Dr+=W[urcourse][rcourse]
            else:
                m=m+1
                #i=i+1
            i+=1
        if Dr!=0:
            predictionDict[urcourse]=float(Nr)/float(Dr)
        else:
            predictionDict[urcourse]=0.0
    #print(predictionDict)

#Sort all the values in dictionary in descending order. If the values are same, then sort ther keys in alphabetical order
    tempList=sorted(predictionDict.items(),key=lambda kv:(-kv[1],kv[0]))

    rItem={}
    kk=k
    if len(tempList)<kk:
        kk=len(tempList)
    for i in range(kk):
        course=tempList[i]
        #print("%s %.5f"%(course[0],course[1]))
        rItem[course[0]]=course[1]
    #print(rItem)
    return rItem

def NewUserPrediction_itemBasedCF(userRatings,n,k,courseIDMap,linesList=None,):
    global userId
    global rating
    global course_name
    userId=0
    rating=1
    course_name=2
    newID=-1
    # n=2
    # k=4
    # if no linesList given then use full user data, otherwise will use given linesList, this may occurs in cross validation
    if linesList==None:
        linesList,courseIDMap,userIDMapInv=loadDataPKL_itemBasedCF("../ItemBasedCF/dataPKL/")
    # return useRatings to the list, and add to linesList, so then we can all mainDo function
    for item in userRatings:
        linesList.append([newID,userRatings[item],item])
        #print([newID,userRatings[item],item])
    pre=mainDo(newID,n,k,linesList)
    return pre



if __name__=="__main__":
    courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL()
    # mainDo(4,2,6)
    simpleTest_itemBasedCF()

    # test,train=splitRatingsKFold(ratings,10,1)
    # recall=oneFoldTest_itemBasedCF(test,train)
    # print(recall)
