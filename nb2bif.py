from set_path import PREFIX_PATH
from sklearn.externals import joblib
from sklearn import naive_bayes
import math
import numpy
from data import SENSOR_NAMES
from data import CLASS_NAMES

def openFile(path):
	return joblib.load(path)

def calculateProbUsingNaiveBayes(x,mean,variance):
	probability = (1/math.sqrt(2*math.pi*variance))*math.e**(-1*((x-mean)**2)/(2*variance))
	return probability

def createProbabilityList(model,selectedClass,domain):
	probList = []
	for i in range(len(SENSOR_NAMES)):
		subList = []
		for j in range(domain['start'],domain['end']):
			subList.append(calculateProbUsingNaiveBayes(j, model.theta_[selectedClass['index']][i], model.sigma_[selectedClass['index']][i]))	
		probList.append(subList)
	return probList

def nb2bif(NaiveBayesModel,selectedClass,domain,probList):
	bif = """<?xml version="1.0" encoding="US-ASCII"?>
 
 
 <!--
 	Bayesian network in XMLBIF v0.3 (BayesNet Interchange Format)
 	Produced by JavaBayes (http://www.cs.cmu.edu/~javabayes/
 	Output created Mon Nov 02 22:40:12**8 GMT-03:00 1998
 -->

 
 
 <!-- DTD for the XMLBIF 0.3 format -->
 <!DOCTYPE BIF [
 	<!ELEMENT BIF ( NETWORK )*>
 	      <!ATTLIST BIF VERSION CDATA #REQUIRED>
 	<!ELEMENT NETWORK ( NAME, ( PROPERTY | VARIABLE | DEFINITION )* )>
 	<!ELEMENT NAME (#PCDATA)>
 	<!ELEMENT VARIABLE ( NAME, ( OUTCOME |  PROPERTY )* ) >
 	      <!ATTLIST VARIABLE TYPE (nature|decision|utility) "nature">
 	<!ELEMENT OUTCOME (#PCDATA)>
 	<!ELEMENT DEFINITION ( FOR | GIVEN | TABLE | PROPERTY )* >
 	<!ELEMENT FOR (#PCDATA)>
 	<!ELEMENT GIVEN (#PCDATA)>
 	<!ELEMENT TABLE (#PCDATA)>
 	<!ELEMENT PROPERTY (#PCDATA)>
 ]>
 
 
 <BIF VERSION="0.3">
 <NETWORK>
	<NAME>NAIVE_BAYES_MODEL</NAME>
	<VARIABLE TYPE  = "nature">
		<NAME>"""+selectedClass['name']+"""</NAME>
		<OUTCOME>true</OUTCOME>
		<OUTCOME>false</OUTCOME>
	</VARIABLE>"""
	for name in SENSOR_NAMES:
		bif = bif +	"""
		<VARIABLE TYPE  = "nature">
			<NAME>""" + name + """</NAME>
		"""
		for i in range(domain['start'],domain['end']):
			bif = bif +	"""
			<OUTCOME>"""+"X"+str(i)+"""</OUTCOME>"""
		bif = bif +"""
		</VARIABLE>"""
	
	bif = bif+"""
	<DEFINITION>
	<FOR>"""+selectedClass['name']+"""</FOR>
		<TABLE>""" + str(NaiveBayesModel.class_prior_[selectedClass['index']]) +" "+ str(1-NaiveBayesModel.class_prior_[selectedClass['index']])+"""</TABLE>
	</DEFINITION>"""
	for i in range(len(SENSOR_NAMES)):
		table = " "
		SUM = 0
		for j in range(domain['start'],domain['end']):
			SUM += probList[i][j]
			subTable = str(probList[i][j]) +" "
			table = table+subTable
		
		#check sum of whole class probability
		print("sensor"+str(i)+", sum="+str(SUM)) 
		
		for j in range(domain['start'],domain['end']):
			subTable = str(1 - probList[i][j]) +" "
			table = table+subTable
		bif = bif + """
			
		<DEFINITION>
		<FOR>""" + SENSOR_NAMES[i] + """</FOR>
		<GIVEN>"""+selectedClass['name']+"""</GIVEN>
		<TABLE>""" + table + """ </TABLE>
		</DEFINITION>"""
	
	bif =  bif + """
	</NETWORK>
	</BIF>"""
	return bif

def writeXML(path,object):
	file = open(path, 'wb')
	file.write(object)


#RUNNING SECTION...

file = openFile(PREFIX_PATH+"NH3/model/nb_model")
NaiveBayesModel = file[4]
#write BIFXML for 6 classes
for i in range(len(CLASS_NAMES)):
	selectedClass = {"name": CLASS_NAMES[i],"index": i} #from "CLASS1" to "CLASS6"
	print(selectedClass['name'])

	domain = {'start':0,'end':2**8}
	print(domain)

	probability = createProbabilityList(NaiveBayesModel,selectedClass,domain)
	bif = nb2bif(NaiveBayesModel,selectedClass,domain,probability)

	writeXML(PREFIX_PATH+"NH3/bifmodel/nb_bifmodel_"+selectedClass['name']+".xml03", bif)
	 
	 
	 