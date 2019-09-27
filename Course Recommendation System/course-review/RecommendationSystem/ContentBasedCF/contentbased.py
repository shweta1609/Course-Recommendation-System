#/usr/local/bin/python

import pandas as pd 
import numpy as np
import math
import sys
import json
import random
from sets import Set

def loadData():
	# load specializations
	filename = '../ContentBasedCF/specializations.txt'
	specializations = []
	if filename:
		with open(filename, 'r') as f:
			specializations = json.load(f)

	# load courses for which we have reviews
	filename = '../ContentBasedCF/coursedetails.txt'
	courses = []
	if filename:
		with open(filename, 'r') as f:
			courses = f.read().splitlines()

	return specializations, courses

# call preprocess before calling this
# get all courses of the specialization that the user has not taken
def getPredictions(usercourses):

	predictions = []
	
	specs, courses = loadData()
	# check which specializations this person might have
	possiblespec = dict() # store count of courses that fit it
	for usercourse in usercourses:
		# search for course number in each specialization
		# usercourse must be the course number, not the name
		for spec in specs:
			courselist = specs[spec]
			for coursename in courselist:
				# check for a match
				if usercourse in coursename:
					# this is a match
					if spec in possiblespec:
						possiblespec[spec] = possiblespec[spec] + 1
					else:
						possiblespec[spec] = 1

	#print possiblespec

	# get most probable spec - the one with most courses matching
	sortedspeclist = sorted(possiblespec, key=possiblespec.get, reverse=True)
	predictedspec = ""
	if sortedspeclist:
		predictedspec = sortedspeclist[0]

	#print predictedspec

	# get all courses for that spec
	speccourses = specs[predictedspec]
	#print speccourses

	# all the courses of this specialization which the user has not taken - add to prediction list
	for speccourse in speccourses:
		# check if the user has already taken this course
		taken = False # default
		for usercourse in usercourses:
			coursenum = usercourse.split(' ')[0]
			if coursenum in speccourse:
				taken = True
				break
		if taken is False:
			# not already taken
			predictions.append(speccourse)

	predictionsset = Set(predictions)

	if len(predictionsset) > 4:
		predictionssetlist = list(predictionsset)
		indices = random.sample(range(0, len(predictionsset) - 1), 4)
		modifiedpredictionset = Set()
		for index in indices:
			course = predictionssetlist[index]
			modifiedpredictionset.add(course)
		predictionsset = modifiedpredictionset

	#print len(predictionsset)
	return predictionsset

# get only the course numbers and return that
# if already only course numbers, keep it the same
def preprocess(usercourses):
	finallist = []
	for usercourse in usercourses:
		if ' ' in usercourse:
			coursenum = usercourse.split(' ')[0]
			finallist.append(coursenum)
		else:
			finallist.append(usercourse)
	return finallist

# return a dictionary for the purpose of integration with the webui
def apiresponse(predictedcourses):
	response = dict()
	for course in predictedcourses:
		response[course] = ""
	return response

def content_based_api(courselist):
	usercoursenumbers = preprocess(courselist)
	predictedcourses = getPredictions(usercoursenumbers)
	response = apiresponse(predictedcourses)
	return response

if __name__=="__main__":

	#usercourses = ["CS-6210 Advanced Operating Systems", "CS-6250 Computer Networks", "CS-6220 Big Data Systems and Analytics", "CS-6262 Network Security"]
	usercourses = ["CS-6210", "CS-6250", "CS-6220", "CS-6262"]

	response = content_based_api(usercourses)
	print response
	
