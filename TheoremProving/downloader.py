from Datasets.utils import *


def download():
    target_folder = 'TheoremProving'
    base_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00249/'
    filenames = ['ml-prove.tar.gz']

    downloader(target_folder, base_url, filenames)


if __name__ == '__main__':
    download()
