#import modules
import math
import sys
import pickle


#arguments
txtfile=sys.argv[1]
userName=sys.argv[2]
userName=int(userName)#for user id are numbers
n=int(sys.argv[3])
k=int(sys.argv[4])


#global variables
uIndex=0
rating=1
course_name=2
#Print=False


#define functions
'''def setPrint():
    global Print
    Print=True

def resetPrint():
    global Print
    Print=False'''


def getUserRatings(myList):
    tempDict={}
    for eachList in myList:
        course=eachList[course_name]
        user=eachList[uIndex]
        userRating=eachList[rating]
        if course in tempDict:
            tempDict[course][user]=float(userRating)
        else:
            #tempDict[course][user]=userRating
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



#Main Function
if __name__=="__main__":
    ratingsFile=open(txtfile,"r+") #Read the .tsv and create a list of lists for each line
    # lines=ratingsFile.read()
    # lines=lines.split('\n')
    # linesList=[]
    # for eachItem in lines:
    #     eachItem=eachItem.split(' ')
    #     if eachItem!=['']:
    #         linesList.append(eachItem)

    with open("dataPKL/user2.pkl",'rb') as f:
        data=pickle.load(f)
    with open("dataPKL/userIDMapInv.pkl",'rb') as f:
        userIDMapInv=pickle.load(f)
    linesList=data
    print(userIDMapInv[418])
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
    itemsList=getItemsList(linesList) #List of all the unique courses in the given .tsv
#Dictionary of all the unrated courses by a user(passed as argv)
#unratedcoursesDict={User:[course1,course2...]}
    unratedcoursesDict=getUnratedcourses(userName,itemsList,coursesDict)
    print(unratedcoursesDict)

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


    newDict={}
    for urcourse in W:
        tempList=[]
        d=W[urcourse]
#Sort all the values in dictionary in descending order. If the values are same, then sort ther keys in alphabetical order
        tempList=[v[0] for v in sorted(d.items(), key=lambda kv:(-kv[1],kv[0]))]
        newDict[urcourse]=tempList

    #if Print==True:
     #   print "NewDict"


#Make prediction for courses with highest pearson correlation for the given user
    predictionDict={}
    for urcourse in newDict:
        Nr=Dr=0.00000
        m=n
        if len(newDict[urcourse]) < n:
            m=len(newDict[urcourse])
        i=0
        while i<m:
            rcourse=newDict[urcourse][i]
            if userName in coursesDict[rcourse]:
#Nr=Summation of Ru,n * Wi,n
#Dr=Summation of Wi,n
#Prediction for user u for item i = Nr/Dr
                Nr+=W[urcourse][rcourse]*coursesDict[rcourse][userName]
                Dr+=W[urcourse][rcourse]
            else:
                m=m+1
            i+=1
        if Dr!=0:
            predictionDict[urcourse]=float(Nr)/float(Dr)
        else:
            predictionDict[urcourse]=0.0
    #print(predictionDict)

#Sort all the values in dictionary in descending order. If the values are same, then sort ther keys in alphabetical order
    tempList=sorted(predictionDict.items(),key=lambda kv:(-kv[1],kv[0]))
    for i in range(k):
        course=tempList[i]
        print("%s %.5f"%(course[0],course[1]))


#close all files
    ratingsFile.close()
