from Datasets.utils import *


def download():
    target_folder = 'MNIST'
    base_url = 'http://yann.lecun.com/exdb/mnist/'
    filenames = ['train-images-idx3-ubyte.gz',
                 'train-labels-idx1-ubyte.gz',
                 't10k-images-idx3-ubyte.gz',
                 't10k-labels-idx1-ubyte.gz']

    downloader(target_folder, base_url, filenames)


if __name__ == '__main__':
    download()
