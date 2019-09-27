from collabFilter import *
#from myUtil import *
import pickle
import numpy as np

def oneFoldTest(testdata,traindata,testUserID,c=4):
	c=c
	#print(np.shape(testdata))
	#print(np.shape(traindata))
	colNum=np.shape(testdata)[1]
	rowTest=np.shape(testdata)[0]
	rowTrain=np.shape(traindata)[0]
	courseNum=colNum/c
	#print(courseNum)

	testdataModified=[]
	removedCourse=[]

	for entry in testdata:
		tookIndex=vectorToCourseTokenList(entry,c,courseNum)
		sel=np.random.choice(tookIndex)
		removedCourse.append(sel)
		entry2=entry.copy()
		for j in range(c):
			entry2[sel*c+j]=0
		testdataModified.append(entry2)
	# print(removedCourse)
	# print(testdataModified)

	ratings=readRatings(traindata)
	#print(testUserID)
	ii=0
	hit=0
	for d in testdataModified:
		prediction=predict_for_new_user(d,ratings,10,verbose=False,topK=4)
		tookIndex=vectorToCourseTokenList(prediction,c,courseNum)
		# print(tookIndex)
		# print(removedCourse[ii])
		if removedCourse[ii] in tookIndex:
			hit+=1
		ii+=1
	recall=float(hit)/(ii)
	return recall 
	pass

def crossValidation(totalFold=10):
	with open("dataPKL/dataVector.pkl",'rb') as f:
		data=pickle.load(f)
	data=np.array(data)
	sumAcc=0
	for i in range(totalFold):
		test,train,uid=split(data,totalFold,i+1)
		sumAcc+=oneFoldTest(test,train,uid)
	print(sumAcc/totalFold)
	return sumAcc/totalFold

def multiTest(time=30):
	sumAcc=0
	for i in range(time):
		Acc=crossValidation()
		sumAcc+=Acc
		print(i,Acc)
	print('---')
	print(sumAcc/time)


def split(dataVector,totalFold=10,thisFold=10):
	length=len(dataVector)
	foldLength=(length//totalFold)

	seq=np.array(range(length))
	np.random.shuffle(seq)

	start=(thisFold-1)*foldLength
	end=thisFold*foldLength
	foldRange=range(start,end)
	outRange1=range(0,start)
	outRange2=range(end,length)
	foldRange=seq[range(start,end)]
	outRange1=seq[range(0,start)]
	outRange2=seq[range(end,length)]
	
	testdata=dataVector[foldRange]
	traindata=np.c_[dataVector[outRange1].T,dataVector[outRange2].T].T
	testUserId=seq[range(start,end)]
	
	return testdata, traindata, testUserId

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

if __name__=="__main__":
	# with open("dataPKL/dataVector.pkl",'rb') as f:
	# 	data=pickle.load(f)
	# data=np.array(data)
	# ratings = readRatings(data)
	# testdata,traindata,testUserId=split(data)
	# oneFoldTest(testdata,traindata,testUserId)
	#crossValidation()
	multiTest()
