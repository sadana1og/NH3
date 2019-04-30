import json
from set_path import PREFIX_PATH
import copy

def loadJSON(path):
	with open(path, "r") as read_file:
		return json.load(read_file)

def compareList(listA, listB):
	if (len(listA) != len(listB)):
		return False
	for i in range(len(listA)):
		if (listA[i] != listB[i]):
			return False
	return True

def findUniqueList(list):
	unique = []
	for i in range(len(list)):
		if (list[i] not in unique):
			unique.append(list[i])
	return unique

def countUnique(list):
	unique = findUniqueList(list)
	uniqueCNT = []
	for i in range(len(unique)):
		CNT = 0
		dict = {}
		for j in range(len(list)):
			if (compare_list(unique[i], list[j])):
				CNT += 1
		dict['sensors'] = unique[i]
		dict['CNT'] = CNT
		uniqueCNT.append(dict)
	return uniqueCNT
	
def getKey(val): 
    return val['CNT']  

def sort(input):
	return sorted(input, key=getKey)


def sumSigificance(list):
	sumList = []
	for i in range(9):
		sum = 0
		for j in range(len(list)):
			sum += list[j][i]
		sumList.append(sum)
	return sumList
	
def writeJSON(path,object):
	file = open(path, 'wb')
	file.write(json.dumps(object))
	
#RUNNING SECTION...

file_path = PREFIX_PATH+"NH3/sig/significance_class4_threshold-09.json"
significance = loadJSON(file_path)
uniqueAndCNT = countUnique(significance)
ranked = sorted(uniqueAndCNT,key=getKey)  
sumCNT = sumSigificance(sig)
writeJSON(file_path[0:-5]+"_count.json",sumCNT)
writeJSON(file_path[0:-5]+"_rank.json",ranked)


