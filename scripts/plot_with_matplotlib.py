import matplotlib.pyplot as plt

from imas2xarray import to_xarray

x_var = 'rho_tor_norm'
y_var = 't_e'
time_var = 'time'

dataset = to_xarray('/pfs/work/g2aho/public/imasdb/test/3/92436/1/', ids='core_profiles')

fig = dataset.plot.scatter(x=x_var, y=y_var, hue=time_var, marker='.')

plt.show()
