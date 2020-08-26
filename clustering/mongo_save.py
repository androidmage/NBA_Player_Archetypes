#%% import libraries
from pymongo import MongoClient
import numpy as np
import pandas as pd

#%% connect to MongoDB
client = MongoClient('mongodb+srv://allenadmin:adminpass@shopping-list-tutorial-5jacx.mongodb.net/mern_shopping?retryWrites=true&w=majority')
db=client.mern_shopping

#%% clear collections
# db['cluster_means'].delete_many({})
# db['players'].delete_many({})

#%% save cluster means
cluster_means = pd.read_csv('clustering/cluster_means.csv')
mean_values = list(cluster_means.T.to_dict().values())
db['cluster_means'].insert_many(mean_values)

#%% save player information with clusters
clustered_players = pd.read_csv('clustering/clustered_players.csv')
players = list(clustered_players.T.to_dict().values())
db['players'].insert_many(players)

#%% close connection
client.close()