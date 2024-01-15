# Artificially modify data for the notebooks
from __future__ import annotations

from imas2xarray import Variable, to_imas, to_xarray

variables = (
    Variable(
        name='ion_temperature',
        ids='core_profiles',
        path='profiles_1d/*/ion/*/temperature',
        dims=['time', 'ion', '$rho_tor_norm'],
    ),
    't_i_ave',
)

ids = 'core_profiles'
path = '.'

for subdir, k in (
    ('2', 1.2),
    ('3', 1.4),
):
    dataset = to_xarray(
        f'{path}/1/data',
        ids=ids,
        variables=variables,
    )
    print(subdir, k)
    dataset['t_i_ave'] *= k
    dataset['ion_temperature'] *= k

    to_imas(
        f'{path}/{subdir}/data',
        dataset=dataset,
        ids=ids,
        variables=variables,
    )
