#%% aggregate player data from each year
import pandas as pd
import numpy as np
df = pd.DataFrame()

names = []
for year in range(2014, 2020):
    yearDf = pd.read_csv('data/playerTotals' + str(year) + '.csv', sep=',')
    names += [name + ' ' + str(year) for name in yearDf['name']]
    df = pd.concat([df, yearDf], axis=0, ignore_index=True)

#%% remove extraneous columns
df.drop(['slug', 'positions', 'name', 'team'], axis=1, inplace=True)
X = df.values

#%% fill in blank columns
from sklearn.impute import SimpleImputer
print(df.isna().any())

imputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=0)
imputer.fit(X)
X = imputer.transform(X)

# #%% encode categorical data
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import OneHotEncoder
# ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
# X = np.array(ct.fit_transform(X))

#%% output combined player totals
df.index = names
df.to_csv('data/combinedPlayerTotals.csv')

#%% feature scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)

#%% output aggregated player data
df = pd.DataFrame(data=X, columns=df.columns)
df.to_csv('data/aggregatedData.csv', float_format='%.3f')