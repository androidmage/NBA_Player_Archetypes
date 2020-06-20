#%% Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%% Importing the dataset
dataset = pd.read_csv('data/aggregatedData.csv', index_col=0)
X = dataset.values
names = dataset.index

#%% Applying PCA
from sklearn.decomposition import PCA
pc_num = 24
model = PCA(n_components = pc_num).fit(X)
X_pc = model.transform(X)
explained_variance = model.explained_variance_ratio_
print(explained_variance.sum())

#%% visualize
pcs = model.components_
pcs_abs = np.absolute(pcs)
feature_num = 10
pc = 1
for row in pcs_abs:
    indices = row.argsort()[-feature_num:][::-1]
    plt.figure(figsize=[35, 15])
    plt.bar(x=dataset.columns[indices], height=pcs[pc-1, indices])
    plt.draw()
    
    pc += 1

plt.show()

#%% save principal components
dataset = pd.DataFrame(X_pc)
dataset.columns = ['PC'+str(name+1) for name in dataset.columns]
dataset.index = names
dataset.to_csv('clustering/pcs.csv', float_format='%.3f')