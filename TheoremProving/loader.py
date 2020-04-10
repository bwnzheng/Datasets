import pandas as pd
from sklearn.model_selection import train_test_split
from Datasets.params import *


def getdataframe():
    return pd.DataFrame(pd.read_csv(DatasetsDir + 'TheoremProving/ml-prove/all-data-raw.csv', header=None))


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
    heuristics: pd.DataFrame = dataframe.iloc[:, range(-5, 0)]  # 选取后五列
    heuristics.rename(columns={53: 1, 54: 2, 55: 3, 56: 4, 57: 5}, inplace=True)

    cls: pd.Series = heuristics.min(axis=1)
    cls_idx = heuristics.idxmin(axis=1)

    for idx, num in enumerate(cls):
        if num == -100:
            cls[idx] = 0
        else:
            cls[idx] = cls_idx[idx]

    # attrs = dataframe.drop(columns=range(53, 58))
    attrs = dataframe

    attrs_train, attrs_test, labels_train, labels_test \
        = train_test_split(attrs.values, cls.values, test_size=kwargs['test_size'])

    return attrs_train, labels_train, attrs_test, labels_test


if __name__ == '__main__':
    load(test_size=0.2)
