#%% Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%% Importing the dataset
dataset = pd.read_csv('clustering/pcs.csv', index_col=0)
X = dataset.values
names = dataset.index

#%% Using the dendrogram to find the optimal number of clusters
import scipy.cluster.hierarchy as sch
dendrogram = sch.dendrogram(sch.linkage(X, method = 'ward'))
plt.title('Dendrogram')
plt.xlabel('Players')
plt.ylabel('Euclidean distances')
plt.show()

#%% Training the Hierarchical Clustering model on the dataset
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters = 11, affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(X)

clusters = pd.DataFrame(y_hc)
clusters.index = names

for cluster in range(0, 10):
    print(clusters.index[clusters[0] == cluster].tolist())
    print()
    print()
    print()
#%% Visualising the clusters
plt.scatter(X[y_hc == 0, 0], X[y_hc == 0, 1], s = 100, c = 'red', label = 'Cluster 1')
plt.scatter(X[y_hc == 1, 0], X[y_hc == 1, 1], s = 100, c = 'blue', label = 'Cluster 2')
plt.scatter(X[y_hc == 2, 0], X[y_hc == 2, 1], s = 100, c = 'green', label = 'Cluster 3')
plt.scatter(X[y_hc == 3, 0], X[y_hc == 3, 1], s = 100, c = 'cyan', label = 'Cluster 4')
plt.scatter(X[y_hc == 4, 0], X[y_hc == 4, 1], s = 100, c = 'magenta', label = 'Cluster 5')
plt.scatter(X[y_hc == 5, 0], X[y_hc == 5, 1], s = 100, c = 'orange', label = 'Cluster 6')
plt.scatter(X[y_hc == 6, 0], X[y_hc == 6, 1], s = 100, c = 'purple', label = 'Cluster 7')
plt.scatter(X[y_hc == 7, 0], X[y_hc == 7, 1], s = 100, c = 'brown', label = 'Cluster 8')
plt.scatter(X[y_hc == 8, 0], X[y_hc == 8, 1], s = 100, c = 'black', label = 'Cluster 9')
plt.scatter(X[y_hc == 9, 0], X[y_hc == 9, 1], s = 100, c = 'tan', label = 'Cluster 10')
plt.scatter(X[y_hc == 10, 0], X[y_hc == 10, 1], s = 100, c = 'maroon', label = 'Cluster 10')
plt.title('Clusters of customers')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()