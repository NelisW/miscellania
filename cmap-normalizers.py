import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

class HistogramNormalize(colors.Normalize):
    def __init__(self, data, vmin=None, vmax=None):
        if vmin is not None:
            data = data[data > vmin]
        if vmax is not None:
            data = data[data < vmax]
            
        sorted_data = np.sort(data.flatten())
        self.sorted_data = sorted_data[np.isfinite(sorted_data)]
        colors.Normalize.__init__(self, vmin, vmax)

    def __call__(self, value, clip=None):
        return np.ma.masked_array(np.searchsorted(self.sorted_data, value) /
                                  len(self.sorted_data))

data = np.linspace(-0.01, 1e-6, 100**2).reshape(100, -1)
normalizer = HistogramNormalize(data)
fig, ax = plt.subplots()

cax = ax.imshow(data, norm=normalizer)
cbar = fig.colorbar(cax)
plt.show()




class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=0):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

data = np.linspace(-0.01, 1e-4, 100**2).reshape(100, -1)
normalizer = MidpointNormalize(midpoint=0)
fig, ax = plt.subplots()

cax = ax.imshow(data, norm=normalizer)
cbar = fig.colorbar(cax)
plt.show()