from problog.program import PrologString
from problog.core import ProbLog
from problog import get_evaluatable
from set_path import PREFIX_PATH

with open(PREFIX_PATH+"NH3/plp/prolog_string1.txt", "r") as read_file:
	prologString = read_file.read()

#RUNNING SECTION...

#prologString = ""
#prologString = loadTextFile(PREFIX_PATH+"NH3/plp/prolog_string.txt")

prologString = prologString + "equal(sensor1,98).\n"
prologString = prologString + "equal(sensor2,98).\n"
prologString = prologString + "equal(sensor3,98).\n"
prologString = prologString + "equal(sensor4,98).\n"
prologString = prologString + "equal(sensor5,98).\n"
prologString = prologString + "equal(sensor6,98).\n"
prologString = prologString + "equal(sensor7,98).\n"
prologString = prologString + "equal(sensor8,98).\n"
prologString = prologString + "equal(sensor9,98).\n"

prologString = prologString + "query(class1).\n"
prologString = prologString + "query(class2).\n"
prologString = prologString + "query(class3).\n"
prologString = prologString + "query(class4).\n"
prologString = prologString + "query(class5).\n"
prologString = prologString + "query(class6).\n"

p = PrologString(prologString)
evaluate = get_evaluatable().create_from(p).evaluate()

print(evaluate)
