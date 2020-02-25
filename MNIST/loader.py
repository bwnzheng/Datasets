import struct
import numpy as np
from sklearn.model_selection import train_test_split

from Datasets.params import *


def load(**kwargs):
    """
    Parameters
    ----------
    load_original : bool, optional (default=True)
        If True, the loader will load the dataset separation setting of the
        original files. If False, the loader will separate the dataset randomly
        by test_size.
    test_size : float, int or None, optional (default=None)
        If float, should be between 0.0 and 1.0 and represent the proportion
        of the dataset to include in the test split. If int, represents the
        absolute number of test samples. If None, the value is set to the
        complement of the train size. If ``train_size`` is also None, it will
        be set to 0.25.
    """
    train_labels_path = DatasetsDir + 'MNIST/train-labels-idx1-ubyte'
    train_images_path = DatasetsDir + 'MNIST/train-images-idx3-ubyte'
    test_labels_path = DatasetsDir + 'MNIST/t10k-labels-idx1-ubyte'
    test_images_path = DatasetsDir + 'MNIST/t10k-images-idx3-ubyte'

    with open(train_labels_path, 'rb') as train_labels:
        magic, n = struct.unpack('>II', train_labels.read(8))
        train_label = np.fromfile(train_labels, dtype=np.uint8)

    with open(train_images_path, 'rb') as train_images:
        magic, num, rows, cols = struct.unpack('>IIII', train_images.read(16))
        train_image = np.fromfile(train_images, dtype=np.uint8).reshape(len(train_label), 784)

    with open(test_labels_path, 'rb') as test_labels:
        magic, n = struct.unpack('>II', test_labels.read(8))
        test_label = np.fromfile(test_labels, dtype=np.uint8)

    with open(test_images_path, 'rb') as test_images:
        magic, num, rows, cols = struct.unpack('>IIII', test_images.read(16))
        test_image = np.fromfile(test_images, dtype=np.uint8).reshape(len(test_label), 784)
    if 'test_size' not in kwargs:
        if kwargs.setdefault('load_original', True):
            return train_image, train_label, test_image, test_label
        else:
            kwargs['test_size'] = 0.2

    labels = np.hstack((train_label, test_label))
    images = np.vstack((train_image, test_image))

    return train_test_split(images, labels, test_size=kwargs['test_size'])


if __name__ == '__main__':
    load(test_size=0.2)
