def itemBasedCF_API(course_list):
	from myUtil_i import loadDataPKL_itemBasedCF, loadDataPKL, loadDataPKL_itemBasedCF
	import numpy as np
	from itemBasedCFAlgs import NewUserPrediction_itemBasedCF
	returnValue={}

	if not ('ratings' in locals()):
		courseFullName,likeMap,userIDMap,userIDMapInv,courseIDMap,ratings=loadDataPKL("../ItemBasedCF/dataPKL/")
	if not ('linesList' in locals()):
		linesList,courseIDMap,userIDMapInv=loadDataPKL_itemBasedCF("../ItemBasedCF/dataPKL/")

	if len(course_list)==0:
		course_list={'CS-6035':[2,2,2,2]}

	newUserInfo={}
	#print(courseIDMap)
	for course in course_list:
		#print(courseIDMap[course])
		if course not in courseIDMap:
			continue
		newUserInfo[course]=str(course_list[course][1])
	#print(newUserInfo)
	
	retN=4
	try:
		k=4
		pre=NewUserPrediction_itemBasedCF(newUserInfo,k,retN,courseIDMap)
	except:
		try:
			k=3
			pre=NewUserPrediction_itemBasedCF(newUserInfo,k,retN,courseIDMap)
		except:
			try:
				k=2
				pre=NewUserPrediction_itemBasedCF(newUserInfo,k,retN,courseIDMap)
			except:
				k=1
				pre=NewUserPrediction_itemBasedCF(newUserInfo,k,retN,courseIDMap)
	#print(pre)

	for i in pre:
		returnValue[i+courseFullName[i]]=None

	return returnValue


if __name__=="__main__":
	course_list={'CS-6300':[1,2,3,4],'CS-6400':[0,3,0,3]}
	course_list={}
	print(itemBasedCF_API(course_list))
	pass