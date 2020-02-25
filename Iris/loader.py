import pandas as pd
from sklearn.model_selection import train_test_split
from Datasets.params import *


def getdataframe():
    return pd.DataFrame(pd.read_csv(DatasetsDir + 'Iris/bezdekIris.data'))


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
