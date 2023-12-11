from imas2xarray import to_imas, to_xarray

variables = ('rho_tor_norm', 'time', 't_e')
ids = 'core_profiles'

dataset = to_xarray(
    '/pfs/work/g2aho/public/imasdb/test/3/92436/1/',
    ids=ids,
    variables=variables,
)

print(dataset['t_e'])
dataset['t_e'] += 1

to_imas(
    '/pfs/work/g2aho/public/imasdb/test/3/92436/1/',
    dataset=dataset,
    ids=ids,
    variables=variables,
)
