from pgmpy.readwrite import XMLBIFReader
from pgmpy.readwrite import XMLBIFWriter
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
import pandas as pd
from set_path import PREFIX_PATH
import pickle
from random import randint
import numpy as np
import json
import copy
import time
from data import SENSOR_NAMES
from data import CLASS_NAMES
from data import SIGNIFICANCE_VECTOR_CLASS

def loadXMLBIF(path):
	reader = XMLBIFReader(path)
	model = reader.get_model()
	print("LOADMODEL: "+str(path))
	"""
	for cpd in model.get_cpds():
		#if(cpd.variable == "SENSOR1"):
		print("CPD of {variable}:".format(variable=cpd.variable))
		print(cpd)
	"""
	return model

def initial():
	global eliminatedModel
	loadedModel1 = loadXMLBIF(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_CLASS1.xml03")
	loadedModel2 = loadXMLBIF(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_CLASS2.xml03")
	loadedModel3 = loadXMLBIF(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_CLASS3.xml03")
	loadedModel4 = loadXMLBIF(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_CLASS4.xml03")
	loadedModel5 = loadXMLBIF(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_CLASS5.xml03")
	loadedModel6 = loadXMLBIF(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_CLASS6.xml03")

	eliminatedModel1 = {"name": "CLASS1","model": VariableElimination(loadedModel1)}
	eliminatedModel2 = {"name": "CLASS2","model": VariableElimination(loadedModel2)}
	eliminatedModel3 = {"name": "CLASS3","model": VariableElimination(loadedModel3)}
	eliminatedModel4 = {"name": "CLASS4","model": VariableElimination(loadedModel4)}
	eliminatedModel5 = {"name": "CLASS5","model": VariableElimination(loadedModel5)}
	eliminatedModel6 = {"name": "CLASS6","model": VariableElimination(loadedModel6)}

	eliminatedModel = [eliminatedModel1, eliminatedModel2, eliminatedModel3, eliminatedModel4, eliminatedModel5, eliminatedModel6]


def getKey(item):
	return item[1]

def scaleUp(list):
	SUM = 0
	for i in range(len(list)):
		SUM += list[i][1]
	for j in range(len(list)):
		list[j][1] = list[j][1]/SUM
	return list

def predictByUsingBayesianModel(evidence):

	""" using
	print("class_: "+ predictByUsingBayesianModel(evidence)["class_"])
	print("proba_: "+str(predictByUsingBayesianModel(evidence)["proba_"]))
	print("rank_: "+str(predictByUsingBayesianModel(evidence)["rank_"]))
	"""
	
	list = []
	for i in range(len(eliminatedModel)):
		list.append([eliminatedModel[i]["name"],eliminatedModel[i]["model"].query(variables=[eliminatedModel[i]["name"]],evidence = evidence)[eliminatedModel[i]["name"]].values[0]])
	rank = sorted(list,key=getKey,reverse=True)
	rank = scaleUp(rank)
	rankList = []
	for i in range(len(CLASS_NAMES)):
		dict = {}
		dict["class_"] = rank[i][0]
		dict["proba_"] = rank[i][1]
		rankList.append(dict)
	class_ = rank[0][0]
	proba_ = rank[0][1]
	return {"class_":class_,"proba_": proba_,"rank_": rankList}

def loadJSON(path):
	with open(path, 'r') as file:
		return json.loads(file.read())

def toVectorListAndClassify(database,selectedClass):
	list = []
	length = len(database)
	for i in range(length):
		if (database[i]['CLASS'] == selectedClass):
			subList = []
			for j in range(len(SENSOR_NAMES)):
				subList.append(database[i][SENSOR_NAMES[j]])
			list.append(subList)
	return list

def toVectorList(database):
	list = []
	length = len(database)
	for i in range(length):
		subList = []
		for j in range(len(SENSOR_NAMES)):
			subList.append(database[i][SENSOR_NAMES[j]])
		list.append(subList)
	return list

def toEvidence(vector, enableVector):
	evidence = {}
	for i in range(len(SENSOR_NAMES)):
		if (enableVector[i] == 1):
			evidence[SENSOR_NAMES[i]] = int(vector[i])
	return evidence

def findSignificanceVector(database,threshold):
	startTime = time.time()
	CNT = 0
	significance = []
	for vector in database:

		#------------------------------------
		# TAKE SO MUCH TIME...
		#------------------------------------

		enableVector = [1,1,1,1,1,1,1,1,1]
		evidence = toEvidence(vector, enableVector)
		predictedValues = predictByUsingBayesianModel(evidence)
		thisClass = predictedValues["class_"]
		thisProb = predictedValues["proba_"]
		
		for i in range(len(enableVector)):
		
			tempEnableVector = copy.deepcopy(enableVector)
			tempEnableVector[i] = 0
			tempEvidence = toEvidence(vector, tempEnableVector)
			tempPredictedValues = predictByUsingBayesianModel(tempEvidence)
			tempClass = tempPredictedValues["class_"]
			tempProb = tempPredictedValues["proba_"]
			
			if((thisClass == tempClass) & (tempProb >= threshold*thisProb)):
				enableVector = copy.deepcopy(tempEnableVector)
				
		significance.append(enableVector)
		elapsedTime = time.time() - startTime
		print(CNT,elapsedTime)
		CNT += 1
	return significance

def writeJSON(path,object):
	file = open(path,'wb')
	file.write(json.dumps(object))

def implementSignificanceDatabase(database,SIGNIFICANCE_VECTOR_CLASS):
	startTime = time.time()
	significanceDatabase = []
	CLASS_CNT = 0
	
	for vector in database:
		VECTOR_CNT = 0
		t = predictByUsingBayesianModel(toEvidence(vector,[1,1,1,1,1,1,1,1,1]))
		print(t["class_"],t["proba_"])
		for i in range(len(CLASS_NAMES)):
			dict = {}
			evidence = toEvidence(vector, SIGNIFICANCE_VECTOR_CLASS[i])
			predict = predictByUsingBayesianModel(evidence)
			for j in range(len(CLASS_NAMES)):
				if (predict["rank_"][j]["class_"] == CLASS_NAMES[i]):
					dict["prob"] = predict["rank_"][j]["proba_"]
					dict["vector"] = vector
					dict["sig_vector"] = SIGNIFICANCE_VECTOR_CLASS[i]
					dict["class"] = CLASS_NAMES[i]
					dict["predict"] = predict
					significanceDatabase.append(dict)
					VECTOR_CNT += 1
			elapsedTime = time.time() - startTime
			print("vector="+str(CLASS_CNT),"class="+str(VECTOR_CNT),"time="+str(elapsedTime),"current="+dict["class"],"prob="+str(dict["prob"]))
		CLASS_CNT +=1
	return significanceDatabase

#RUNNING SECTION...

initial()

database = loadJSON(PREFIX_PATH+"NH3/db/database_1.json")
#select class
selectedClass = 6
#threshold
threshold = 0.9
databaseList1 = toVectorListAndClassify(database,selectedClass)

#all classes
databaseList2 = toVectorList(database)

"""
significance = findSignificanceVector(databaseList1,threshold)
writeJSON(PREFIX_PATH+"NH3/sig/test_significance_class"+str(selectedClass)+"_threshold-"+str(threshold)+".json",significance)


significanceProbability = implementSignificanceDatabase(databaseList2,SIGNIFICANCE_VECTOR_CLASS)
writeJSON(PREFIX_PATH+"NH3/sig/significance_prob.json",significanceProbability)
"""






