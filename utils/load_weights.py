import h5py
import sys
import numpy as np

sys.path.append('../')

def quantize(weights):
    abs_weights = np.abs(weights)
    vmax = np.max(abs_weights)
    s = vmax / 127.
    qweights = weights / s
    qweights = np.round(qweights)
    qweights = qweights.astype(np.float32)
    return qweights, s


def weight_loader(weight_file, by_name=False):
    assert by_name, 'argument by_name must be true!'
    weights = {}
    scale = {}
    f = h5py.File(weight_file, mode='r')
    # f = f['model_weights']
    try:
        layers = f.attrs['layer_names']
    except:
        raise ValueError("weights file must contain attribution: 'layer_names'")
    for layer_name in layers:
        g = f[layer_name]
        count = 0
        for weight_name in g.attrs['weight_names']:
            weight_value = g[weight_name].value
            name = str(weight_name).split("'")[1]
            if count == 0:
                weight_value, s = quantize(weight_value)
                scale[name] = s
                count += 1
            weights[name] = weight_value
    return weights, scale