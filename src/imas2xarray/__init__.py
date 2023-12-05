from __future__ import annotations

from ._io import H5Handle, to_xarray
from ._lookup import VariableConfigLoader, var_lookup
from ._models import IDSPath, VariableConfigModel
from ._models import IDSVariableModel as Variable
from ._rebase import (
    rebase_all_coords,
    rebase_on_grid,
    rebase_on_time,
    rezero_time,
    squash_placeholders,
    standardize_grid,
    standardize_grid_and_time,
)

__author__ = 'Stef Smeets'
__email__ = 's.smeets@esciencecenter.nl'
__version__ = '0.2.0'

__all__ = [
    'H5Handle',
    'IDSPath',
    'Variable',
    'rebase_all_coords',
    'rebase_on_grid',
    'rebase_on_time',
    'rezero_time',
    'squash_placeholders',
    'standardize_grid',
    'standardize_grid_and_time',
    'to_xarray',
    'var_lookup',
    'VariableConfigLoader',
    'VariableConfigModel',
]
