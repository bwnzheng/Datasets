import matplotlib.pyplot as plt
from .loader import *


def preview():
    X_train, y_train, _, _ = load(load_originial=True)

    fig, ax = plt.subplots(
        nrows=2,
        ncols=5,
        sharex=True,
        sharey=True, )

    ax = ax.flatten()
    for i in range(10):
        img = X_train[y_train == i]
        instance_num = int(np.floor(np.size(img, 0) * np.random.rand()))
        img = img[instance_num].reshape(28, 28)
        ax[i].imshow(img, cmap='Greys', interpolation='nearest')
        ax[i].set_title(instance_num.__str__())

    ax[0].set_xticks([])
    ax[0].set_yticks([])

    plt.tight_layout()
    plt.show()


def showinstance(num):
    X_train, y_train, _, _ = load(load_originial=True)
    img = X_train[num].reshape(28, 28)
    plt.imshow(img, cmap='Greys', interpolation='nearest')
    plt.xlabel(str(y_train[num]))
    plt.xticks([])
    plt.yticks([])
    plt.show()


if __name__ == '__main__':
    showinstance(777)
