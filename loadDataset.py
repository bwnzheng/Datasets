from Datasets import *

load_fns = {
    'iris': Iris.load,
    'MNIST': MNIST.load,
    'glass': Glass.load,
    'ionosphere': Ionosphere.load
}


def load_dataset(name: str, **kwargs):
    return load_fns[name](**kwargs)
