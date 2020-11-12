import numpy as np
from sklearn.metrics import r2_score


class Mathimatical1:
    def __init__(self, **entries):
        self.__dict__.update(entries)


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