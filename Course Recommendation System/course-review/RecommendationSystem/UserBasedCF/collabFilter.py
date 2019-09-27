import sys
import json
import string
import math
import csv
import pickle
from scipy import spatial
import numpy as np
from myUtil_u import *

ratings = {} # initialize an empty ratings dictionary
final_list=[]
sum=0
def main():

    with open("../PopularCourseRecommend/dataPKL/dataVector.pkl",'rb') as f:
        data=pickle.load(f)
    user1 = str(sys.argv[1])
    user2 = str(sys.argv[2])
    k = int(sys.argv[3])
    vec=[[]]
    inside_vec=[]
 
    ratings = readRatings(data)
    #print "readRatings output", ratings
    sim = similarity(ratings[int(user1)], ratings[int(user2)])
    print "**********************"
 
    #print "sim = ", sim
    nearest = nearestNeighbors(int(user1), ratings, k)
    #print ratings[int(user1)]
    #print "nearestNeighbors: ", nearest
    #print "****************"
    x = ratings[int(user1)]




    #prediction = predict(nearest, ratings,user1,k,inside_vec,vec)
    prediction = predict2(nearest, ratings,user1,k,verbose=True,topK=4)
    #print "prediction for user" ": ", prediction

    interpret(prediction)

def readRatings(data):

    for i in range(0,np.shape(data)[0]):
        user_id=i
        #for j in range(i+1,257):
        ratings[user_id]=data[i]
    #print ratings
    return ratings


def similarity(user_ratings_1, user_ratings_2):

    
    result= 1 - spatial.distance.cosine(user_ratings_1, user_ratings_2)

    return result


def nearestNeighbors(user_id, all_user_ratings, k):
    
    nearest=[]
    for each_user in all_user_ratings:
        if int(user_id)!=each_user:
            nearest.append((each_user,similarity(ratings[int(user_id)],all_user_ratings[each_user])))
              
    nearest=sorted(nearest, key=lambda user: user[1] ,reverse=True)
        
    return nearest[0:k]

def predict(nearest, ratings,user1,k,inside_vec,vec):
    
    
    x = ratings[int(user1)]
    for i in range(0,k):
        for key,value in ratings.items():
            if key==nearest[i][0]:
                y = ratings[key]
                #print y
                #print len(x)
                for j in range(0,len(x)):
                    #print x[j]
                    #print y[j]
                    inside_vec.append((x[j]+y[j])/2)
                    #vec.append(inside_vec)
                    #print vec
                vec.append(inside_vec)
                #print vec
                inside_vec=[]
    #print vec
    #print vec
    #print "======================"
    # for i in range(1,len(vec)):
    #     for j in range(0,len(vec[i])):
    #         final
    sum=0
    for j in range(0,117):
        for i in range(1,len(vec)):
            sum=float(sum+vec[i][j])
        #print sum
        sum=float(sum/k)
        #print sum
        final_list.append(float(("%.1f" % sum)))
        #print final_list


    #print final_list
    #print final_list


    return vec


def predict2(nearest,ratings,user,k,noDuplicate=True,verbose=False,topK=-1,c=4):
    user=int(user)
    new_user_ratings=ratings[user]
    c=c #attr per course

    #if verbose print the neighoubrs information
    if verbose:
        print(nearest)

    column_number=np.shape(ratings[0])[0]
    prediction=np.zeros(column_number) 
    total_weight=np.zeros(column_number/c) # = each course has a weight
    for i in range(k):
        nid=nearest[i][0]
        nsim=nearest[i][1]
        nRatings=ratings[nid]
        for courseID in range(column_number/c):
            courseTookFlag=False
            for j in range(c):
                courseTookFlag=courseTookFlag or (nRatings[c*courseID+j]!=0)
            #print(courseTookFlag)
            if courseTookFlag:
                total_weight[courseID]+=nsim
        nRatings=np.array(ratings[nid])*nsim
        prediction=prediction+nRatings
    for courseID in range(column_number/c):
        for j in range(c):
            if total_weight[courseID]>0:
                prediction[courseID*c+j]/=total_weight[courseID]
    prediction=np.around(prediction,decimals=1)

    #if noDuplicate remove the course this user already took
    if noDuplicate:
        for i in range(column_number/c):
            courseTookFlag=False
            for j in range(c):
                 courseTookFlag=courseTookFlag or (new_user_ratings[c*i+j]!=0) # if all course attr is non zero, the this course took before
            if courseTookFlag:
                for j in range(c):
                    prediction[c*i+j]=0

    #if topK=-1 recommend all noDuplicated course, otherwise return # = topK courses (if enough)
    if topK>=0:
        remain_course_index=[]
        all_course_record=np.zeros(column_number/c)
        for i in range(column_number/c):
            for j in range(c):
                all_course_record[i]+=prediction[c*i+j]
        sortIndex=np.argsort(all_course_record)[::-1]
        predictionTopK=np.zeros(column_number) 
        for i in range(topK):
            index=sortIndex[i]
            for j in range(c):
                predictionTopK[index*c+j]=prediction[index*c+j]
        prediction=predictionTopK
    
    return prediction

def predict_for_new_user(new_user_ratings,all_user_ratings,k,noDuplicate=True,verbose=False,topK=-1,c=4):
    c=c #attr per course
    nearest=nearestNeighbors_for_new_user(new_user_ratings,all_user_ratings,k)
    
    #if verbose print the neighoubrs information
    if verbose:
        print(nearest)
    
    column_number=np.shape(ratings[0])[0]
    prediction=np.zeros(column_number) 
    total_weight=np.zeros(column_number/c) # = each course has a weight
    for i in range(k):
        nid=nearest[i][0]
        nsim=nearest[i][1]
        nRatings=ratings[nid]
        for courseID in range(column_number/c):
            courseTookFlag=False
            for j in range(c):
                courseTookFlag=courseTookFlag or (nRatings[c*courseID+j]!=0)
            #print(courseTookFlag)
            if courseTookFlag:
                total_weight[courseID]+=nsim
        nRatings=np.array(ratings[nid])*nsim
        prediction=prediction+nRatings
    for courseID in range(column_number/c):
        for j in range(c):
            if total_weight[courseID]>0:
                prediction[courseID*c+j]/=total_weight[courseID]
    prediction=np.around(prediction,decimals=1)

    #if noDuplicate remove the course this user already took
    if noDuplicate:
        for i in range(column_number/c):
            courseTookFlag=False
            for j in range(c):
                 courseTookFlag=courseTookFlag or (new_user_ratings[c*i+j]!=0) # if all course attr is non zero, the this course took before
            if courseTookFlag:
                for j in range(c):
                    prediction[c*i+j]=0

    #if topK=-1 recommend all noDuplicated course, otherwise return # = topK courses (if enough)
    if topK>=0:
        remain_course_index=[]
        all_course_record=np.zeros(column_number/c)
        for i in range(column_number/c):
            for j in range(c):
                all_course_record[i]+=prediction[c*i+j]
        sortIndex=np.argsort(all_course_record)[::-1]
        predictionTopK=np.zeros(column_number) 
        for i in range(topK):
            index=sortIndex[i]
            for j in range(c):
                predictionTopK[index*c+j]=prediction[index*c+j]
        prediction=predictionTopK
    
    return prediction

def nearestNeighbors_for_new_user(userRatings, all_user_ratings, k):
    nearest=[]
    for each_user in all_user_ratings:
            nearest.append((each_user,similarity(userRatings,all_user_ratings[each_user])))
              
    nearest=sorted(nearest, key=lambda user: user[1] ,reverse=True)
        
    return nearest[0:k]

def interpret(pred,c=4):
    c=c #attr per course
    print "********"
    print "interpretation of prediction vector"
    #courseFullName, userIDMap, userIDMapInv, userIDMapMap, userIDMapMapInv, courseIDMap, courseIDMapInv, difficultyMapInv, likeMapInv, loadMapInv, sentimentMapInv=loadDataPKL()
    courseFullName, userIDMap, userIDMapInv, userIDMapMap, userIDMapMapInv, courseIDMap, courseIDMapInv=loadDataPKL()
    #for onePred in pred:
    if c==3:
        for i in range(len(pred)/3):
            diff=pred[i*3]
            like=pred[i*3+1]
            load=pred[i*3+2]
            if diff==0 and like==0 and load==0:
                continue
            print(courseIDMapInv[i]+": "+'difficulty '+str(diff)+'; like '+str(like)+'; load '+str(load))

            #print("                     "+difficultyMapInv[diff]+'     '+likeMapInv[like]+'     '+loadMapInv[load])
    
    if c==4:
        for i in range(len(pred)/4):
            diff=pred[i*4]
            like=pred[i*4+1]
            load=pred[i*4+2]
            sentiment=pred[i*4+3]
            if diff==0 and like==0 and load==0 and sentiment==0:
                continue
            print(courseIDMapInv[i]+": "+'difficulty '+str(diff)+'; like '+str(like)+'; load '+str(load)+"; sentiment"+str(sentiment))
            


    print('---')
   
def test():
    with open("dataPKL/dataVector.pkl",'rb') as f:
        data=pickle.load(f)
    ratings = readRatings(data)
    userRatings=ratings[0]

    prediction=predict_for_new_user(userRatings,ratings,4,verbose=True,topK=4)
    interpret(prediction)


if __name__ == '__main__':
    main()
    #test()
