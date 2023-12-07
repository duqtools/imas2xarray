from imas2xarray import to_imas, to_xarray

x_var = 'rho_tor_norm'
y_var = 't_e'
time_var = 'time'

variables = (x_var, y_var, time_var)

dataset = to_xarray(
    './data',
    ids='core_profiles',
    variables=variables,
)

print(dataset['t_e'])
dataset['t_e'] += 1

to_imas(
    './data',
    dataset=dataset,
    ids='core_profiles',
    variables=variables,
)
