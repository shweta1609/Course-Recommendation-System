def popularCourseRecommend(percent_data=1):
	percent_data=percent_data 
	import pickle
	import numpy as np
	from myUtil_p import loadDataPKL,vectorToCourseTokenList, interpret

	c=4
	with open("../PopularCourseRecommend/dataPKL/dataVector.pkl",'rb') as f:
		data=pickle.load(f)
	courseFullName, userIDMap, userIDMapInv, userIDMapMap, userIDMapMapInv, courseIDMap, courseIDMapInv=loadDataPKL("../PopularCourseRecommend/dataPKL/")

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


	courseNum=len(courseIDMap)
	c=4

	row=np.shape(data)[0]
	col=np.shape(data)[1]

	averageData=np.zeros(col)
	dataCount=np.zeros(courseNum)
	courseRatings=np.zeros(courseNum)
	#courseShow=np.zeros(courseNum)
	for i in range(row):
		averageData=averageData+data[i]
		courseShow=vectorToCourseTokenList(data[i],c,courseNum)
		for courseID in courseShow:
			dataCount[courseID]+=1
	for i in range(courseNum):
		div=dataCount[i]
		if div<10:
			div=10.0
		for j in range(c):
			averageData[i*c+j]/=div
	averageData=np.around(averageData,decimals=1)
	#print(averageData)
	#print(interpret(averageData))
	#
	#print(dataCount)
	for i in range(courseNum):
		#for j in range(c):
		courseRatings[i]+=averageData[i*c+1]
	#print(courseRatings)

	sortInd1=np.argsort(dataCount)[::-1]
	sortInd2=np.argsort(courseRatings)[::-1]
	#print(sortInd1)
	#print(sortInd2)
	#for i in range(len(sortInd1)):
	#	print(courseIDMapInv[sortInd1[i]])
	#print("---")
	#for i in range(len(sortInd1)):
	#	print(courseIDMapInv[sortInd1[i]],courseFullName[courseIDMapInv[sortInd1[i]]], courseRatings[sortInd1[i]],dataCount[sortInd1[i]])
	#print(courseFullName)
	#print(courseIDMapInv)

	returnValue={}
	for i in range(4):
		courseID=sortInd1[i]
		value=None
		# for j in range(c):
		# 	value.append(prediction[courseID*c+j].item())
		# value.append(4-prediction[courseID*c].item())
		# value.append(prediction[courseID*c+1].item())
		# value.append(4-prediction[courseID*c+2].item())
		# value.append(prediction[courseID*c+3].item())
		returnValue[courseIDMapInv[sortInd1[i]]+courseFullName[courseIDMapInv[sortInd1[i]]]]=value

	return returnValue




	pass


if __name__=="__main__":
	print(popularCourseRecommend())
	pass