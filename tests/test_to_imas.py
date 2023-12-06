from __future__ import annotations

import os

import pytest

from imas2xarray import H5Handle


@pytest.fixture
def dataset():
    ds = 123
    return ds


@pytest.mark.xfail
def test_to_imas(dataset, tmpdir):
    # copy data to tempdir

    h = H5Handle(tmpdir / 'my_data')

    ids = 'core_profiles'
    variables = 'zeff', 't_e'

    path = (h.path / ids).with_suffix('h5')
    assert path.exists()
    mtime1 = os.stat(path).st_mtime

    h.to_imas(dataset, ids=ids, variables=variables)

    assert (h.path / ids).with_suffix('h5').exists()
    mtime2 = os.stat(path).st_mtime
    assert mtime2 != mtime1
