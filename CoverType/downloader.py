from Datasets.utils import *


def download():
    target_folder = 'CoverType'
    base_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/'
    filenames = ['covtype.data.gz',
                 'covtype.info',
                 'old_covtype.info']

    downloader(target_folder, base_url, filenames)


if __name__ == '__main__':
    download()
