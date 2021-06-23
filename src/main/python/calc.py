import numba as nb
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical
import matplotlib.lines as mlines
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report

from settings import Settings, BASE_DIR


config = Settings()


@nb.njit()
def distance(x):
    return np.linalg.norm(x)


model1 = load_model(BASE_DIR / 'new_model.h5')

# метки от 2 до 7, сеть хочет от 0 до 5
labels_mapping = {label - 2: label for label in range(2, 9)}
labels_mapping_reverse = {label: label - 2 for label in range(2, 9)}


def clear_data(_data):
    _data = list(filter(lambda i: len(i) > 1, map(lambda i: i.replace('\n', ''), _data)))
    _data = [[float(value) for value in row.split(' ')] for row in _data]
    _data_clear = []
    for row in _data:
        _type = row[0] if len(row) == 4 else None
        _coords = row[1:] if len(row) == 4 else row
        if _type not in range(2, 8):
            _type = 8.
        _row_clear = [_type, *_coords]
        _data_clear.append(_row_clear)
    _data_clear = np.array(_data_clear)
    return _data_clear


@nb.njit()
def prepare_xtest_njit(_a, _b):
    _norm_matrix = _a - _b
    dat = np.zeros((_norm_matrix.shape[0], 4))
    for idx, row in enumerate(_norm_matrix):
        dat[idx] = np.array([row[0], row[1], row[2], distance(row)], dtype=np.float64)
    return dat[dat[:, 3].argsort()][:30]


@nb.njit(nb.float64[:, :, ::1](nb.float64[::, ::]))
def run_prepare_njit(_src_data):
    res = np.zeros((_src_data.shape[0], 30, 4))
    for idx, item in enumerate(_src_data):
        res[idx] = prepare_xtest_njit(_src_data, item)
    return res


def excel_export(_f, yt, yp, _data, _test):
    _test_labels = [row[0] for row in _data]
    _result = [[_test[i][0], _test[i][1], _test[i][2], yt[i], yp[i]] for i in range(len(_data))]
    _df = pd.DataFrame(_result, columns=['X', 'Y', 'Z', 'Target_Type', 'Predicted_Type'])
    _df.to_excel(_f)


def process_file(_file):
    data = clear_data(open(_file, 'r').readlines())
    Y_test = data[:, 0]
    test = data[:, 1:]

    X_test = run_prepare_njit(test)
    _Y_test = [labels_mapping_reverse[label] for label in Y_test]
    x_test = X_test.reshape(len(X_test), 120)
    y_test = to_categorical(np.asarray(_Y_test), num_classes=7)

    _Y_test = np.array([labels_mapping[y] for y in np.argmax(y_test, axis=1)])

    return {
        'data': data,
        'test': test,
        'x_test': x_test,
        '_Y_test': _Y_test,
    }


def plot_data(coords, types, types_test, data):
    _f = pd.DataFrame([
        [
            coords[i][0], coords[i][1], coords[i][2], types[i]
        ]
        for i in range(len(coords))
    ], columns=['X', 'Y', 'Z', 'T'])
    _all = np.unique(_f[['T']])

    points_z_axis = _f[_f['T'] != 7]['Z']
    z_lim = (float(points_z_axis.min()), float(points_z_axis.max()))

    types_match = config.types_match

    legend = [
        mlines.Line2D([], [], color=types_match[str(pred_type)][1], marker=types_match[str(pred_type)][0],
                      linestyle='None', markersize=5, label=types_match[str(pred_type)][2])
        for pred_type in _all
    ]

    return [
               (
                   _f.loc[_f['T'] == pred_type]['X'],
                   _f.loc[_f['T'] == pred_type]['Y'],
                   _f.loc[_f['T'] == pred_type]['Z'],
                   types_match[str(pred_type)][1],
                   types_match[str(pred_type)][0],
               ) for pred_type in _all
           ], legend, z_lim, (types_test, types, data, coords)


def raw_types(_file_data):
    data = _file_data['data']
    test = _file_data['test']
    _Y_test = _file_data['_Y_test']

    return plot_data(test, _Y_test, _Y_test, data)


def prediction(x_test):
    return np.array([labels_mapping[y] for y in list(model1.predict_classes(x_test))])


def predict_types(_file_data):
    data = _file_data['data']
    test = _file_data['test']
    _Y_test = _file_data['_Y_test']
    Y_pred = _file_data['Y_pred']

    return *plot_data(test, Y_pred, _Y_test, data), classification_report(_Y_test, Y_pred)
