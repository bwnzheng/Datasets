import pandas as pd
from sklearn.model_selection import train_test_split
from Datasets.params import *


def getdataframe():
    return pd.DataFrame(pd.read_csv(DatasetsDir + 'Glass/glass.data'))


def load(**kwargs):
    """
    Parameters
    ----------
    test_size : float, int or None, optional (default=None)
        If float, should be between 0.0 and 1.0 and represent the proportion
        of the dataset to include in the test split. If int, represents the
        absolute number of test samples. If None, the value is set to the
        complement of the train size. If ``train_size`` is also None, it will
        be set to 0.25.
    """
    dataframe = getdataframe()
    dataframe['class'].replace(
        {1: 'building_windows_float_processed',
         2: 'building_windows_non_float_processed',
         3: 'vehicle_windows_float_processed',
         4: 'vehicle_windows_non_float_processed(none in this database)',
         5: 'containers',
         6: 'tableware',
         7: 'headlamps'},
        inplace=True
    )
    fn_dict = {
        'RI': (lambda x: (x - 1.5184) / 0.0030),
        'Na': (lambda x: (x - 13.4079) / 0.8166),
        'Mg': (lambda x: (x - 2.6845) / 1.4424),
        'Al': (lambda x: (x - 1.4449) / 0.4993),
        'Si': (lambda x: (x - 72.6509) / 0.7745),
        'K': (lambda x: (x - 0.4971) / 0.6522),
        'Ca': (lambda x: (x - 8.9570) / 1.4232),
        'Ba': (lambda x: (x - 0.1750) / 0.4972),
        'Fe': (lambda x: (x - 0.0570) / 0.0974),
    }
    dataframe.drop(columns='Id', inplace=True)
    for k in fn_dict:
        dataframe[k] = dataframe[k].transform(fn_dict[k])

    class_names = dataframe['class'].unique()

    idx = 0
    print('class information:')
    for name in class_names:
        dataframe['class'].replace(name, idx, inplace=True)
        print(idx, name, sep=': ', end='\n')
        idx = idx + 1

    labels = dataframe['class']
    attrs = dataframe.iloc[:, range(len(dataframe.axes[1]) - 1)]

    attrs_train, attrs_test, labels_train, labels_test \
        = train_test_split(attrs.values, labels.values, test_size=kwargs['test_size'])

    return attrs_train, labels_train, attrs_test, labels_test


if __name__ == '__main__':
    load(test_size=0.2)
