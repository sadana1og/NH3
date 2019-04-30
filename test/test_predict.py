from sklearn.externals import joblib
from sklearn import naive_bayes
import math
import numpy

def openFile(FilePath):
    file = joblib.load(FilePath)
    return file

file = openFile('C:/Users/User/Documents/test_files/nb_model')
naive_bayes_model = file[4]
"""
print("VECTOR OF CLASS1 FROM DATASET:")
print("")
for i in range(0,1000):
	cls = naive_bayes_model.predict([file[0][i]])
	if(cls == [[1]]):
		#print(cls)
		print(file[0][i])
"""
"""
list = []
count = 0
for class_ in file[1]:
	if (class_ == [[1]]):
		list.append(file[0][count])
	count +=1

test = file[0][0]
#print(test)
s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
s6 = 0
for i in range(len(list)):
	a = naive_bayes_model.predict([list[i]])
	if(a==[1]):
		s1 = s1+1
	if(a==[2]):
		s2 = s2+1
	if(a==[3]):
		s3 = s3+1
	if(a==[4]):
		s4 = s4+1
	if(a==[5]):
		s5 = s5+1
	if(a==[6]):
		s6 = s6+1

print(s1)
print(s2)
print(s3)
print(s4)
print(s5)
print(s6)
"""
a = [ 83. , 68.,  70. , 89., 138., 157., 196. , 81. , 68.]
print(naive_bayes_model.predict([a]))