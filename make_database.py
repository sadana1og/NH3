from set_path import PREFIX_PATH
from sklearn.externals import joblib
import json
from data import SENSOR_NAMES

def loadFileByJoblib(path):
	return joblib.load(path)
	
def checkAndReturnLength(list1, list2):
	if(len(list1) != len(list1)):
		raise "length is not equal"
	return len(list1)

def createJSONObject(vector,class_):
	array = {}
	for i in range(len(SENSOR_NAMES)):
		array[SENSOR_NAMES[i]] = vector[i]
	array["CLASS"] = class_
	return array

def createJSONList(vectorList,classList):
	list = []
	for i in range(checkAndReturnLength(vectorList,classList)):
		list.append(createJSONObject(vectorList[i],classList[i]))
	return list

def writeJSON(path,object):
	file = open(path,'wb')
	file.write(json.dumps(object))

#RUNNING SECTION...

file = loadFileByJoblib(PREFIX_PATH+'NH3/model/nb_model')
vectorDataset = file[0]
classDataset = file[1]
length = checkAndReturnLength(vectorDataset,classDataset)
database = createJSONList(vectorDataset,classDataset)
writeJSON(PREFIX_PATH+'NH3/db/database_2.json',database)

#find max and min
def findMaxAndMin():
	#list = []
	for i in range(9):
		max = 0
		for j in range(1000):
			if (max<vectorDataset[j][i]):
				max = vectorDataset[j][i]
		list.append(max)
		print("sensor"+str(i+1)+" max="+str(max))

	print("\n")
	for i in range(9):
		min = 255
		for vector in vectorDataset:
			if(vector[i] < min):
				min = vector[i]
		print("sensor"+str(i+1)+" min="+str(min))

findMaxAndMin()
