
import pandas as pd
import plotly.express as px
from sklearn import preprocessing
import numpy as np
from sklearn.decomposition import PCA
from load_dataset import load_dataset

X = load_dataset()

print(X)

#standardize the data by centering and scaling
scaler = preprocessing.StandardScaler().fit(load_dataset())
X_scaled = scaler.transform(X)
pca = PCA()

#plot the variance
#variance = pca.explained_variance_ratio_ * 100
#var_per_component = pd.DataFrame({'Percent Variance Explained': variance, 'Component': range(1,97)})
#fig = px.scatter(var_per_component, x="Component", y="Percent Variance Explained")
#fig.show()

#plot the scores
components = pca.fit_transform(X_scaled).T
df = pd.DataFrame({'PC1': components[0], 'PC2': components[1]})
df['Label'] = 24 * ['Wild Type'] + 24 * ['Knock Down']
fig = px.scatter(df, x='PC1', y='PC2', color='Label')
fig.show()