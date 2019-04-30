from sklearn.externals import joblib
from sklearn import naive_bayes
import json
import optimize_bif 

def openFile(FilePath):
	file = joblib.load(FilePath)
	return file

file = openFile('nb_model')
naive_bayes_model = file[4]

with open("database_1.json", "r") as read_file:
    db = json.load(read_file)

Database = optimize_bif.toVectorList(db)

enableVector = [1,1,1,1,1, 1,1,1,1]

cnt = 0
for v in Database:
	evi = optimize_bif.toEvidence(v,enableVector)
	b = optimize_bif.bif_predict(optimize_bif.eliminatedModel, evi)
	c = naive_bayes_model.predict([v])
	if (c[0] != int(b["class_"][-1])):
		cnt +=1
		#print(c[0],b["class_"][-1])

print("vector: "+ str(len(Database)))
print("Not match: "+ str(cnt))

"""
output

Isadas-MacBook-Air-3:NH3 Isada$ python2 test_function_predict.py 
LOADMODEL: nb_bifmodel_CLASS1.xml03
LOADMODEL: nb_bifmodel_CLASS2.xml03
LOADMODEL: nb_bifmodel_CLASS3.xml03
LOADMODEL: nb_bifmodel_CLASS4.xml03
LOADMODEL: nb_bifmodel_CLASS5.xml03
LOADMODEL: nb_bifmodel_CLASS6.xml03
9.53674316406e-07
/usr/local/Cellar/python@2/2.7.15_3/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/sklearn/base.py:251: UserWarning: Trying to unpickle estimator GaussianNB from version 0.20.0 when using version 0.20.2. This might lead to breaking code or invalid results. Use at your own risk.
  UserWarning)
vector: 319
Not match: 16
error = 5.016%
"""