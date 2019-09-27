def userBasedCF_API(course_list,percent_data=1):
	percent_data=percent_data 
	#this controls how much data to use, if smaller than 1, than randonly cur some data
	#if larger than 1, than some data will be depilcated


	from collabFilter import predict_for_new_user,readRatings
	from myUtil_u import loadDataPKL,vectorToCourseTokenList
	import numpy as np
	import pickle
	
	#course_list = {'', []}
	returnValue={}
	
	courseFullName, userIDMap, userIDMapInv, userIDMapMap, userIDMapMapInv, courseIDMap, courseIDMapInv=loadDataPKL("../PopularCourseRecommend/dataPKL/")

	if len(course_list)==0:
		course_list={'CS-6035':[2,2,2,2]}

	courseNum=len(courseIDMap)
	c=4
	userDataVector=np.zeros(courseNum*4)

	for course in course_list:
		if course not in courseIDMap:
			continue
		courseID=courseIDMap[course]
		for j in range(c):
			userDataVector[courseID*c+j]=course_list[course][j]
	with open("../PopularCourseRecommend/dataPKL/dataVector.pkl",'rb') as f:
		data=pickle.load(f)

	#change data size
	if not percent_data==1:
		if percent_data<1:
			rows=np.shape(data)[0]
			chooseList=np.arange(rows)
			chooseNum=int(percent_data*rows)
			np.random.shuffle(chooseList)
			dataNew=[]
			for i in range(chooseNum):
				dataNew.append(data[chooseList[i]])
			data=dataNew
		else:
			rows=np.shape(data)[0]
			addNum=int(percent_data*rows)-rows
			for i in range(addNum):
				addInd=np.random.choice(rows)
				data.append(data[addInd])
			#print(np.shape(data))
		
	ratings = readRatings(data)
	prediction=predict_for_new_user(userDataVector,ratings,8,verbose=True,topK=4)
	coursetookID=vectorToCourseTokenList(prediction,c,courseNum)
	
	for i in range(len(coursetookID)):
		courseID=coursetookID[i]
		value=[]
		# for j in range(c):
		# 	value.append(prediction[courseID*c+j].item())
		value.append(4-prediction[courseID*c].item())
		value.append(prediction[courseID*c+1].item())
		value.append(4-prediction[courseID*c+2].item())
		value.append(prediction[courseID*c+3].item())
		returnValue[courseIDMapInv[coursetookID[i]]+courseFullName[courseIDMapInv[coursetookID[i]]]]=value

	return returnValue



if __name__=="__main__":
	course_list={'CS-6035':[1,2,3,4],'CS-6210':[0,3,0,3]}
	#course_list={}
	pred=userBasedCF_API(course_list)
	print(pred)
