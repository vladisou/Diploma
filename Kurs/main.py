import Coordinates
from geopy.distance import geodesic
import xgboost as xgb
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


city_center_coordinates = [50.4642, 30.4665]


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def median_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.median(np.abs((y_true - y_pred) / y_true)) * 100


def print_metrics(prediction, val_y):
    r2 = r2_score(val_y, prediction)
    print('')
    print('R: ', r2)
    print('')
    print('MeanAbsErr: {:.3} %'.format(mean_absolute_percentage_error(val_y, prediction)))
    print('MedAbsErr: {:.3} %'.format(median_absolute_percentage_error(val_y, prediction)))


df = pd.read_csv("resultDataset.csv", encoding='utf-8')

df = df.loc[(df['distance'] < 10000)]

df['priceMetr'] = df['priceMetr'].round(0)
df['distance'] = df['distance'].round(0)
df['azimuth'] = df['azimuth'].round(0)

first_quartile = df.quantile(q=0.25)
third_quartile = df.quantile(q=0.75)
IQR = third_quartile - first_quartile
outliers = df[(df > (third_quartile + 1.5 * IQR)) | (df < (first_quartile - 1.5 * IQR))].count(axis=1)
outliers.sort_values(axis=0, ascending=False, inplace=True)

outliers = outliers.head(100)
df.drop(outliers.index, inplace=True)

y = df['priceMetr']

features = [
    'floor',
    'totalArea',
    'livingArea',
    'kitchenArea',
    'floorCount',
    'distance',
    'azimuth'
]

X = df[features]


hm = sns.heatmap(X.corr(),
               cbar=True,
                 annot=True)

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)


rf_model = RandomForestRegressor(n_estimators=900,
                                 n_jobs=-1,
                                 bootstrap=True,
                                 criterion='mse',
                                 max_features=7,
                                 random_state=1,
                                 min_samples_split=2,
                                 oob_score=True,
                                 min_samples_leaf=5
                                 )

print(rf_model)


rf_model.fit(train_X, train_y)

rf_prediction = rf_model.predict(val_X).round(0)

print_metrics(rf_prediction, val_y)

xgb_model = xgb.XGBRegressor(objective='reg:gamma',
                             learning_rate=0.07,
                             n_estimators=600,
                             nthread=-1,
                             eval_metric='gamma-nloglik'
                             )

xgb_model.fit(train_X, train_y)


xgb_prediction = xgb_model.predict(val_X).round(0)
print_metrics(xgb_prediction, val_y)

prediction = rf_prediction * 0.5 + xgb_prediction * 0.5
print_metrics(prediction, val_y)


importances = rf_model.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf_model.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

print("Rating of importance attribute:")
for f in range(X.shape[1]):
    print("%d. %s (%f)" % (f + 1, features[indices[f]], importances[indices[f]]))

plt.figure()
plt.title("Attribute importance")
plt.bar(range(X.shape[1]), importances[indices], color="g", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.xlim([-1, X.shape[1]])
plt.show()



flat = pd.DataFrame({
    'floor': [20],
    'totalArea': [66],
    'livingArea': [24],
    'kitchenArea': [19],
    'floorCount': [25],
    'latitude': [50.5054845396644],
    'longitude': [30.414619445800785]
})

flat['distance'] = list(
    map(lambda x,y: geodesic(city_center_coordinates, [x, y]).meters, flat['latitude'], flat['longitude']))
flat['azimuth'] = list(map(lambda x, y: Coordinates.get_azimuth(x, y), flat['latitude'], flat['longitude']))
flat['distance'] = flat['distance'].round(0)
flat['azimuth'] = flat['azimuth'].round(0)

flat = flat.drop('latitude', axis=1)
flat = flat.drop('longitude', axis=1)

rf_prediction_flat = rf_model.predict(flat).round(0)
xgb_prediction_flat = xgb_model.predict(flat).round(0)

price = (rf_prediction_flat * 0.5 + xgb_prediction_flat * 0.5) * flat['totalArea'][0]

print(f'Price: {int(price[0].round(-3))} uah')
