import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

from imas2xarray import to_xarray, standardize_grid_and_time

runs = 1, 2, 3

ids = 'core_profiles'

x_var = 'rho_tor_norm'
y_var = 't_i_ave'
time_var = 'time'

ds_list = []

for run in runs:
    path = f'/pfs/work/g2aho/public/imasdb/test/3/92436/{run}/'

    ds = to_xarray(path, ids=ids, variables=(x_var, y_var, time_var))
    ds_list.append(ds)

ds_list = standardize_grid_and_time(ds_list, grid_var=x_var, time_var=time_var)

dataset = xr.concat(ds_list, pd.Index(runs, name='run'))

fig = dataset.plot.scatter(x=x_var, y=y_var, hue='time', col='run', marker='.')

plt.show()
