import os
import gzip
import tarfile
import contextlib
import time
from six.moves.urllib import request
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

from .params import *


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
                if os.path.isfile(filepath.replace('.gz', '')):  # 如果gzip文件已经被解压了
                    print('file %s already exists' % filename.replace('.gz', ''))
                elif os.path.isfile(filepath) and os.path.getsize(filepath) == expected_filesize:
                    # 如果没有被解压，而且gzip文件确实存在，而且文件大小相符（已下载完成）
                    print('%s exists, unzip...' % filename)
                    unzip_gz(filepath)
                    del_file(filepath)
                # 运行到这里有两种情况：1gzip文件已经被解压2gzip文件没有被下载
                if os.path.isfile(filepath.replace('.gz', '')):  # 如果到目前为止gzip文件已经被解压了
                    filename = filename.replace('.gz', '')
                    filepath = filepath.replace('.gz', '')
                    if tarfile.is_tarfile(filepath):  # 如果被解压的文件是tar文件
                        if not os.path.isdir(filepath.replace('.tar', '')):  # 如果tar文件没有被解压
                            print('extract %s ...' % filename)
                            extract_tar(filepath)
                            del_file(filepath)
                    continue

            else:
                if os.path.isfile(filepath) and os.path.getsize(filepath) == expected_filesize:
                    print('file %s already exists' % filename)
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

        filename = filename.replace('.gz', '')
        filepath = filepath.replace('.gz', '')

        if filename.endswith('.tar'):
            print('extract %s ...' % filename)
            extract_tar(filepath)
            del_file(filepath)


def unzip_gz(file_path):
    target_path = file_path.replace(".gz", "")
    target_file = gzip.GzipFile(file_path)
    open(target_path, "wb+").write(target_file.read())
    target_file.close()


def extract_tar(file_path):
    if tarfile.is_tarfile(file_path):
        target_path = os.path.dirname(file_path)
        file = tarfile.open(file_path)
        file.extractall(target_path)
        file.close()


def del_file(path):
    os.remove(path)
