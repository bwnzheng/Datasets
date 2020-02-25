import contextlib
import time
from six.moves.urllib import request
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

from Datasets.utils import *
from Datasets.params import *


def download():
    target_path = os.path.join(DatasetsDir, 'MNIST')
    base_url = 'http://yann.lecun.com/exdb/mnist/'
    filenames = ['train-images-idx3-ubyte.gz',
                 'train-labels-idx1-ubyte.gz',
                 't10k-images-idx3-ubyte.gz',
                 't10k-labels-idx1-ubyte.gz']
    print('target path: %s' % target_path)

    for filename in filenames:
        url = base_url + filename
        filepath = os.path.join(target_path, filename)

        print('downloading %s:' % filename)

        with contextlib.closing(request.urlopen(url)) as f:
            expected_filesize = int(f.headers['content-length'])
            print('expected file size:%d' % expected_filesize)
            if os.path.isfile(filepath) and os.path.getsize(filepath) == expected_filesize:
                print('%s exists, unzip...' % filename)
                unzip_gz(filepath)
                del_file(filepath)
                continue
            elif os.path.isfile(filepath.replace('.gz', '')):
                print('file already exists')
                continue

        time.sleep(3)

        widgets = ['{}: '.format(filename), Percentage(), ' ', Bar(), ' ', ETA(),
                   ' ', FileTransferSpeed()]
        progress_bar = ProgressBar(widgets=widgets,
                                   maxval=expected_filesize).start()

        def reporthook(count, blockSize, totalSize):
            progress_bar.update(min(count * blockSize, totalSize))

        request.urlretrieve(url, filepath, reporthook=reporthook)
        progress_bar.finish()

        downloaded_filesize = os.path.getsize(filepath)
        assert expected_filesize == downloaded_filesize, ' '.join((
            'expected file size is {}, but the actual size of the downloaded file',
            'is {}.')).format(expected_filesize, downloaded_filesize)

        print('unzip %s ...' % filename)
        unzip_gz(filepath)
        del_file(filepath)


if __name__ == '__main__':
    download()
