import numpy as np
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from hyperopt import hp, tpe
from hyperopt.fmin import fmin
import pandas as pd

df = pd.read_csv("resultDataset.csv", encoding='utf-8')

df = df.loc[(df['distance'] < 10000)]

df['priceMetr'] = df['priceMetr'].round(0)
df['distance'] = df['distance'].round(0)
df['azimuth'] = df['azimuth'].round(0)
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




train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)


def hyperopt_xgb_score(params):
    clf = XGBClassifier(**params)
    current_score = cross_val_score(clf, X, y, cv=3).mean()
    print(current_score, params)
    return -current_score


simple_space_xgb = {
    'n_estimators': hp.choice('n_estimators', range(100, 1000)),
    'eta': hp.quniform('eta', 0.025, 0.5, 0.025),
    'max_depth': hp.choice('max_depth', np.arange(1, 14, dtype=int)),
}



best = fmin(fn=hyperopt_xgb_score, space=simple_space_xgb, algo=tpe.suggest, max_evals=10)
print('best:')
print(best)