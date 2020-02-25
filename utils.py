import os
import gzip


def unzip_gz(file_path):
    target_path = file_path.replace(".gz", "")
    target_file = gzip.GzipFile(file_path)
    open(target_path, "wb+").write(target_file.read())
    target_file.close()


def del_file(path):
    os.remove(path)
