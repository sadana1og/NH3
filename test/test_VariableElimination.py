from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianModel
import numpy as np
import pandas as pd
values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),columns=['A', 'B', 'C', 'D', 'E'])
model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
model.fit(values)
inference = VariableElimination(model)
phi_query = inference.query(['A', 'B'])
print(phi_query)