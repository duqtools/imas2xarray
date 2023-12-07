from imas2xarray import to_imas, to_xarray

variables = ('rho_tor_norm', 'time', 't_e')
ids = 'core_profiles'

dataset = to_xarray(
    './data',
    ids=ids,
    variables=variables,
)

print(dataset['t_e'])
dataset['t_e'] += 1

to_imas(
    './data',
    dataset=dataset,
    ids=ids,
    variables=variables,
)
