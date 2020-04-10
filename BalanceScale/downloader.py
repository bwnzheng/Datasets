from Datasets.utils import *


def download():
    target_folder = 'TheoremProving'
    base_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/balance-scale/'
    filenames = ['Index',
                 'balance-scale.data',
                 'balance-scale.names']

    downloader(target_folder, base_url, filenames)


if __name__ == '__main__':
    download()
