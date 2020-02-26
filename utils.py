import os
import gzip
import contextlib
import time
from six.moves.urllib import request
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

from params import *


def downloader(target_folder, base_url, filenames):
    target_path = os.path.join(DatasetsDir, target_folder)

    print('target path: %s' % target_path)

    for filename in filenames:
        url = base_url + filename
        filepath = os.path.join(target_path, filename)

        print('downloading %s:' % filename)

        with contextlib.closing(request.urlopen(url)) as f:
            expected_filesize = int(f.headers['content-length'])
            print('expected file size:%d' % expected_filesize)
            if filepath.endswith('.gz'):
                if os.path.isfile(filepath.replace('.gz', '')):
                    print('file already exists')
                    continue
                elif os.path.isfile(filepath) and os.path.getsize(filepath) == expected_filesize:
                    print('%s exists, unzip...' % filename)
                    unzip_gz(filepath)
                    del_file(filepath)
                    continue
            else:
                if os.path.isfile(filepath) and os.path.getsize(filepath) == expected_filesize:
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

        if filename.endswith('.gz'):
            print('unzip %s ...' % filename)
            unzip_gz(filepath)
            del_file(filepath)


def unzip_gz(file_path):
    target_path = file_path.replace(".gz", "")
    target_file = gzip.GzipFile(file_path)
    open(target_path, "wb+").write(target_file.read())
    target_file.close()


def del_file(path):
    os.remove(path)
