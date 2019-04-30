from sklearn.externals import joblib
import math
import numpy

nb = joblib.load('C:/Users/User/Documents/test_files/nb_model')
#print(type(nb[4]))
#print(nb)


# create bnb
from sklearn import naive_bayes
#bnb = naive_bayes.BernoulliNB()
bnb = nb[4]

#predict prob
#probabilities_predByBNB = bnb.predict_log_proba(Xdash)
#dfcopy['CHURNPROB_BNB'] = [math.e**(r[0]) for r in  probabilities_predByBNB]
"""
labelEncoders = {
"CURR_PKG_NM":le4CURR_PKG_NM,
"AVG_PACK_FEE":le4AVG_PACK_FEE,
"CHANNEL":le4CHANNEL,
"SWON_BY":le4SWON_BY,
"RTR_CD":le4RTR_CD,
"ZONE_EN":le4ZONE_EN,
"PROVINCE_EN":le4PROVINCE_EN,
"DEVICE_BRAND":le4DEVICE_BRAND,
"DEVICE_MODEL":le4DEVICE_MODEL,
"SEGMENT_AND_NO_ID":le4SEGMENT_AND_NO_ID,
"USAGE0_FLAG":le4USAGE0_FLAG,
"USAG_TYPE":le4USAG_TYPE,
"CPA_FLAG":le4CPA_FLAG,
"REG_FLAG":le4REG_FLAG,
"BILL_AMPHR": le4BILL_AMPHR,
"BILL_PROVN":le4BILL_PROVN,
"PP_ARPU_Avg.3M":le4PP_ARPU_Avg_3M,
"PP_AOU(Days)":le4PP_AOU_Days,
"AIRTIME_ADV_PAID_FLAG":le4AIRTIME_ADV_PAID_FLAG,
"DEVICE_ADV_PAID_FLAG":le4DEVICE_ADV_PAID_FLAG,
"ADV_PAID_FLAG":le4ADV_PAID_FLAG,
"BAD_CUSTOMER_FLAG":le4BAD_CUSTOMER_FLAG
}
"""
#uncomment to create xml

#print(bnb.feature_log_prob_)
#print(bnb.class_log_prior_[0])


def bnb2pgm(bnb, labelEncoders, format = 'json'):
	
	#df is pandas object which imported from excel file
     pgm = {}
     pgm['V'] = [str(c) for c in df.columns]
     pgm['E'] = [["BAD_CUSTOMER", C] for C in pgm['V']]
     pgm['V'].append("BAD_CUSTOMER")
     pgm['Vdata'] = {}
     feature_log_prob = bnb.feature_log_prob_
     for i in range(0,df.columns.size):
         c = str(df.columns[i])
         pgm['Vdata'][c] = {}
         pgm['Vdata'][c]["ord"] = i
         pgm['Vdata'][c]["numoutcomes"] = 2
         pgm['Vdata'][c]["vals"] = [str(v) for v in list(labelEncoders[c].transform(labelEncoders[c].classes_))]
         pgm['Vdata'][c]["parents"] = ["BAD_CUSTOMER"]
         pgm['Vdata'][c]["children"] = None
         pgm['Vdata'][c]["cprob"] = {}
         featureDomainSize  = len(pgm['Vdata'][c]["vals"])
         
         baseIndexOfFeaturei = sum(labelEncoders[str(df.columns[j])].classes_.size for j in range(0,i))
         
         pgm['Vdata'][c]["cprob"]["['true']"] = [math.e**(feature_log_prob[0][baseIndexOfFeaturei + d]) for d in range(0,featureDomainSize)]
         
         pgm['Vdata'][c]["cprob"]["['false']"] = [math.e**(feature_log_prob[1][baseIndexOfFeaturei + d]) for d in range(0,featureDomainSize)]
     
     pgm['Vdata']["BAD_CUSTOMER"] = {}
     pgm['Vdata']["BAD_CUSTOMER"]["ord"] = df.columns.size
     pgm['Vdata']["BAD_CUSTOMER"]["numoutcomes"] = 2
     pgm['Vdata']["BAD_CUSTOMER"]["vals"] = ["true", "false"]
     pgm['Vdata']["BAD_CUSTOMER"]["parents"] = None
     pgm['Vdata']["BAD_CUSTOMER"]["children"] = [str(c) for c in df.columns]
     pgm['Vdata']["BAD_CUSTOMER"]["cprob"] = [math.e**(bnb.class_log_prior_[0]), 1 -math.e**(bnb.class_log_prior_[0])]
     
     if format == 'json':
         return pgm
     
     # return XML BIF  (BayesNet Interchange Format)
     bif = """<?xml version="1.0" encoding="US-ASCII"?>
 
 
 <!--
 	Bayesian network in XMLBIF v0.3 (BayesNet Interchange Format)
 	Produced by JavaBayes (http://www.cs.cmu.edu/~javabayes/
 	Output created Mon Nov 02 22:40:15 GMT-03:00 1998
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
     <NAME>CHURNMODEL</NAME>""" 
     
     for V in pgm['V']:
         bif = bif + """
         <VARIABLE TYPE  = "nature">
         	<NAME>""" + V + """</NAME>"""
         
         bif = bif + " ".join(["<OUTCOME>" + str(value) + "</OUTCOME>" for value in pgm["Vdata"][V]["vals"]])
         
         bif = bif + """
         </VARIABLE>
         """
     for V in pgm['V']:
         if V == "BAD_CUSTOMER":
             bif =  bif + """
             <DEFINITION>
             	<FOR>BAD_CUSTOMER</FOR>
             	<TABLE>""" + str(pgm['Vdata']["BAD_CUSTOMER"]["cprob"][0]) + " "  + str(pgm['Vdata']["BAD_CUSTOMER"]["cprob"][1]) + """</TABLE>
             </DEFINITION>
             """
             
             bif =  bif + """
             </NETWORK>
             </BIF>
             """
         else:
             table  = pgm['Vdata'][V]["cprob"]["['true']"] +  pgm['Vdata'][V]["cprob"]["['false']"]
             table = [str(v) for v in table]
             table = " ".join(table)
             bif = bif + """
             <DEFINITION>
             	<FOR>""" + V + """</FOR>
             	<GIVEN>""" + "BAD_CUSTOMER" + """</GIVEN>
             	<TABLE>""" + table + """ </TABLE>
             </DEFINITION>
             """
     
     
     return bif

#pgm = bnb2pgm(bnb, labelEncoders, "bif")
apple = 1
orange = 2
mongo = 3
fruit = { "apple" : apple, "orange": orange, "mongo": mongo}
#print(fruit['apple'])

#
a = []
for i in range(1000):
	a.append(nb[4].predict([nb[0][i]])[0])

#print(a)
#print(len(nb[0]))
#print(len(nb[1]))
#print(len(nb[2]))
#print(len(nb[3]))
def naive_bayes_prob(x,mean,variance):
	a = 1/math.sqrt(2*math.pi*variance)
	b = math.e**(-1*((x-mean)**2)/(2*variance))
	return a*b

print(naive_bayes_prob(74,86.2,9.7**2))

"""
print("class_prior_")
print(nb[4].class_prior_)
print("class_count_")
print(nb[4].class_count_)
print("theta_")
print(nb[4].theta_)
print("sigma_")
print(nb[4].sigma_)
print("epsilon_")
print(nb[4].epsilon_)
"""

print("testing")
i = 0
sum = 0
mean = nb[4].theta_[0][0]
var = nb[4].sigma_[0][0]
print(mean)
print(var)
#print(naive_bayes_prob(100,mean,var))
while(i!=255):
	#print(naive_bayes_prob(i,mean,var))
	sum += naive_bayes_prob(i,mean,var)
	i += 1
	

#print(i)

print(sum)
print(math.sqrt(var))

print(naive_bayes_prob(98,mean,var))

"""
import numpy as np
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
Y = np.array([1, 1, 1, 2, 2, 2])
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(X, Y)
print(clf.predict([[-0.8, -1]]))
clf_pf = GaussianNB()
clf_pf.partial_fit(X, Y, np.unique(Y))
print(clf_pf.predict([[-0.8, -1]]))

print("class_prior_")
print(clf.class_prior_)
print("class_count_")
print(clf.class_count_)
print("theta_")
print(clf.theta_)
print("sigma_")
print(clf.sigma_)
print("epsilon_")
print(clf.epsilon_)

mean = clf.theta_[0][0]
var = clf.sigma_[0][0]
print(naive_bayes_prob(1000000,mean,var))


"""









