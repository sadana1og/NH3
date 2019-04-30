from sklearn.externals import joblib
from sklearn import naive_bayes
import math
import numpy as np

def openFile(FilePath):
    file = joblib.load(FilePath)
    return file

file = openFile('C:/Users/User/Documents/test_files/dst_model')

#for i in range (0,1000):
#	print("---------------------------------------------")
#	print(str(i)+" | "+str(file[0][i]) +" => "+str(file[1][i]))
#	print("---------------------------------------------")
"""
print("classes_")
print(file[4].classes_)
print("feature_importances_")
print(file[4].feature_importances_)
print("max_features_")
print(file[4].max_features_)
print("n_classes_")
print(file[4].n_classes_)
print("n_features_")
print(file[4].n_features_)
print("n_outputs_")
print(file[4].n_outputs_)
"""
#print("tree_")
#print(file[4].tree_)
"""

n_nodes = file[4].tree_.node_count
children_left = file[4].tree_.children_left
children_right = file[4].tree_.children_right
feature = file[4].tree_.feature
threshold = file[4].tree_.threshold


# The tree structure can be traversed to compute various properties such
# as the depth of each node and whether or not it is a leaf.
node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
is_leaves = np.zeros(shape=n_nodes, dtype=bool)
stack = [(0, -1)]  # seed is the root node id and its parent depth
while len(stack) > 0:
    node_id, parent_depth = stack.pop()
    node_depth[node_id] = parent_depth + 1

    # If we have a test node
    if (children_left[node_id] != children_right[node_id]):
        stack.append((children_left[node_id], parent_depth + 1))
        stack.append((children_right[node_id], parent_depth + 1))
    else:
        is_leaves[node_id] = True

print("The binary tree structure has %s nodes and has "
      "the following tree structure:"
      % n_nodes)
for i in range(n_nodes):
    if is_leaves[i]:
        print("%snode=%s leaf node." % (node_depth[i] * "\t", i))
    else:
        print("%snode=%s test node: go to node %s if X[:, %s] <= %s else to "
              "node %s."
              % (node_depth[i] * "\t",
                 i,
                 children_left[i],
                 feature[i],
                 threshold[i],
                 children_right[i],
                 ))
print()

# First let's retrieve the decision path of each sample. The decision_path
# method allows to retrieve the node indicator functions. A non zero element of
# indicator matrix at the position (i, j) indicates that the sample i goes
# through the node j.

node_indicator = file[4].decision_path(X_test)

# Similarly, we can also have the leaves ids reached by each sample.

leave_id = file[4].apply(X_test)

# Now, it's possible to get the tests that were used to predict a sample or
# a group of samples. First, let's make it for the sample.

sample_id = 0
node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                    node_indicator.indptr[sample_id + 1]]

print('Rules used to predict sample %s: ' % sample_id)
for node_id in node_index:
    if leave_id[sample_id] == node_id:
        continue

    if (X_test[sample_id, feature[node_id]] <= threshold[node_id]):
        threshold_sign = "<="
    else:
        threshold_sign = ">"

    print("decision id node %s : (X_test[%s, %s] (= %s) %s %s)"
          % (node_id,
             sample_id,
             feature[node_id],
             X_test[sample_id, feature[node_id]],
             threshold_sign,
             threshold[node_id]))

# For a group of samples, we have the following common node.
sample_ids = [0, 1]
common_nodes = (node_indicator.toarray()[sample_ids].sum(axis=0) ==
                len(sample_ids))

common_node_id = np.arange(n_nodes)[common_nodes]

print("\nThe following samples %s share the node %s in the tree"
      % (sample_ids, common_node_id))
print("It is %s %% of all nodes." % (100 * len(common_node_id) / n_nodes,))
"""
#"""
test = [ 75. , 71. , 58. ,105., 106., 126.,  54.,  76.]
print([test])
print(file[4].decision_path([test]))
print(file[4].apply([test]))
print(file[4].predict([test]))
print(file[4].predict_proba([test]))
#"""