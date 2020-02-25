from .loader import getdataframe


def preview(n=10):
    dataframe = getdataframe()
    dataframe.info()
    print(dataframe.head(n))


if __name__ == '__main__':
    preview()
