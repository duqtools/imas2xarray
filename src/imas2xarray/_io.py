"""Handle = H5Handle(path='/afs/eufus.eu/user/g/g2ssmee/imas2xarray/data')

dataset = handle.get_variables(variables=(x_var, y_var, time_var))
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Sequence

import h5py
import numpy as np

from ._lookup import var_lookup
from ._rebase import squash_placeholders

if TYPE_CHECKING:
    import xarray as xr

    from imas2xarray import IDSVariableModel


def deconstruct_path(path) -> tuple[str, list[slice]]:
    h5path: list[str] = []
    slices: list[slice] = []

    delimiter = '&'
    array_symbol = '[]'

    for part in path.split('/'):
        if part == '*':
            slices.append(slice(None))
            h5path[-1] += array_symbol
        elif part.isdigit():
            slices.append(slice(int(part)))
            h5path[-1] += array_symbol
        else:
            h5path.append(part)

    return delimiter.join(h5path), slices


def to_xarray(
    raw_data,
    variables: Sequence[str | IDSVariableModel],
    **kwargs,
) -> xr.Dataset:
    """Return dataset for given variables.

    Parameters
    ----------
    raw_data : ...
    variables : Sequence[str | IDSVariableModel]]
        Dictionary of data variables

    Returns
    -------
    ds : xr.Dataset
        Return query as Dataset
    """
    xr_data_vars: dict[str, tuple[list[str], np.ndarray]] = {}

    variables = var_lookup.lookup(variables)

    for var in variables:
        h5path, slices = deconstruct_path(var.path)

        print(h5path, slices)

        arr = raw_data[h5path]

        if len(slices) == 0:
            xr_data_vars[var.name] = (var.dims, arr)
        else:
            xr_data_vars[var.name] = ([*var.dims], arr[*slices])

    ds = xr.Dataset(data_vars=xr_data_vars)  # type: ignore

    return ds


class H5Handle:

    def __init__(self, path: Path):
        self.path = Path(path)

    def get(self, ids: str = 'core_profiles') -> h5py.File:
        """Map the data to a dict-like structure.

        Parameters
        ----------
        ids : str, optional
            Name of profiles to open

        Returns
        -------
        h5py.File
        """
        data_file = (self.path / ids).with_suffix('.h5')
        assert data_file.exists()

        return h5py.File(data_file, 'r')[ids]

    def get_all_variables(
        self,
        extra_variables: Sequence[IDSVariableModel] = [],
        squash: bool = True,
        ids: str = 'core_profiles',
        **kwargs,
    ) -> xr.Dataset:
        """Get all known variables from selected ids from the dataset.

        This function looks up the data location from the
        `imas2xarray.var_lookup` table

        Parameters
        ----------
        variables : Sequence[IDSVariableModel]
            Extra variables to load in addition to the ones known through the config.
        squash : bool
            Squash placeholder variables

        Returns
        -------
        ds : xarray
            The data in `xarray` format.
        **kwargs
            These keyword arguments are passed to `IDSMapping.to_xarray()`

        Raises
        ------
        ValueError
            When variables are from multiple IDSs.
        """

        idsvar_lookup = var_lookup.filter_ids(ids)
        variables = list(
            set(list(extra_variables) + list(idsvar_lookup.keys())))
        return self.get_variables(variables,
                                  squash,
                                  empty_var_ok=True,
                                  **kwargs)

    def get_variables(
        self,
        variables: Sequence[str | IDSVariableModel],
        squash: bool = True,
        **kwargs,
    ) -> xr.Dataset:
        """Get variables from data set.

        This function looks up the data location from the
        `imas2xarray.var_lookup` table, and returns

        Parameters
        ----------
        variables : Sequence[Union[str, IDSVariableModel]]
            Variable names of the data to load.
        squash : bool
            Squash placeholder variables

        Returns
        -------
        ds : xarray
            The data in `xarray` format.
        **kwargs
            These keyword arguments are passed to `IDSMapping.to_xarray()`

        Raises
        ------
        ValueError
            When variables are from multiple IDSs.
        """
        var_models = var_lookup.lookup(variables)

        idss = {var.ids for var in var_models}

        if len(idss) > 1:
            raise ValueError(
                f'All variables must belong to the same IDS, got {idss}')

        ids = var_models[0].ids

        raw_data = self.get(ids)

        ds = to_xarray(raw_data, variables=var_models, **kwargs)

        if squash:
            ds = squash_placeholders(ds)

        return ds
