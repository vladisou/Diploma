import Coordinates
from geopy.distance import geodesic
import xgboost as xgb
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt


df = pd.read_csv("resultDataset.csv", encoding='utf-8')

y = df['priceMetr'].sort_values()

x = range(len(y))
ax = plt.gca()
ax.bar(x,y, align='edge')
plt.show()

normalized_X = preprocessing.normalize(x)

ax = plt.gca()
ax.bar(normalized_X,y, align='edge')
plt.show()
