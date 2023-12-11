from __future__ import annotations

from pathlib import Path

from imas2xarray import to_xarray

DATA_DIR = Path(__file__).parent / 'hdf5' / 'data'


def test_to_xarray_missing_placeholder(tmpdir):
    ids = 'core_profiles'
    variables = ('t_e',)  # misses time, rho_tor_norm

    dataset = to_xarray(DATA_DIR, variables=variables, ids=ids)

    assert 'time' in dataset
    assert 'rho_tor_norm' in dataset
