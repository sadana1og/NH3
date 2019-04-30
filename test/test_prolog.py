from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable

p = PrologString("""
coin(c1).
0.4::heads(C); 0.6::tails(C) :- coin(C).
win :- heads(C).

query(win).
""")

a = get_evaluatable().create_from(p).evaluate()

print(a)

"""
#input vector(sampling from model file data) -> class 5 (fact)
vector = [70,58,37,130,87,139,164,39,76]

#rule
#class1 pattern = [0,1,0,0,0,1,1,0,1]
evidence = make_evdience(vector,pattern)
#evidence = [sensor2:58,sensor6:139,sensor7:164,sensor9:76]
bif_query(evidence)::class1 :- s2(58),s6(139),s7(164),s9(76)

#class2 pattern =  [0,1,0,1,0,0,1,0,1]
evidence = make_evdience(vector,pattern)
#evidence = [sensor2:58,sensor4:130,sensor7:164,sensor9:76]
bif_query(evidence)::class2 :- s2(58),s4(130),s7(164),s9(76)

... do same until 6 classes



"CLASS": 5,
"SENSOR9": 76.0,
"SENSOR8": 39.0
"SENSOR1": 70.0
"SENSOR3": 37.0
"SENSOR2": 58.0
"SENSOR5": 87.0
"SENSOR4": 130.0
"SENSOR7": 164.0
"SENSOR6": 139.0

"""