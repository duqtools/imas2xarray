from __future__ import annotations

import os
import shutil
from pathlib import Path

from imas2xarray import to_imas, to_xarray

DATA_DIR = Path(__file__).parent / 'hdf5' / 'data'


def test_to_imas(tmpdir):
    filename = 'core_profiles.h5'
    filepath = tmpdir / filename

    shutil.copy(DATA_DIR / filename, filepath)

    ids = 'core_profiles'
    variables = ('rho_tor_norm', 'time', 't_e')

    dataset = to_xarray(tmpdir, variables=variables, ids=ids)

    assert filepath.exists()
    mtime1 = os.stat(filepath).st_mtime

    to_imas(tmpdir, dataset=dataset, ids=ids, variables=variables)

    assert filepath.exists()
    mtime2 = os.stat(filepath).st_mtime

    assert mtime2 != mtime1
