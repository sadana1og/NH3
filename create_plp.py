from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable
import json
from set_path import PREFIX_PATH
from data import SENSOR_NAMES

def loadJSON(path):
	with open(path, "r") as read_file:
		return json.load(read_file)

def toStringForm(vector,sigVector):
	string = ""
	for i in range(len(vector)):
		if (sigVector[i]!=0):
			string = string +"equal("+SENSOR_NAMES[i].lower()+","+str(int(vector[i]))+")"
			if (i!=len(SENSOR_NAMES)-1):
				string = string + ", "
	string = string + ".\n"
	return string

def createRule(string,database):
	for item in database:
		string = string + str(item['prob'])+"::"+item['class'].lower()+" :- "+ toStringForm(item["vector"],item["sig_vector"])
	return string

def writeTextFile(path,object):
	file = open(path,mode="w") 
	file.write(object)

#RUNNING SECTION...

database = loadJSON(PREFIX_PATH+"NH3/sig/significance_prob.json")
prologString = ""
prologString = createRule(prologString,database)
writeTextFile(PREFIX_PATH+"NH3/plp/prolog_string1.txt",prologString)



