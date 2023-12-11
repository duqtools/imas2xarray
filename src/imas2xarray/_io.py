"""Handle = H5Handle(path='/afs/eufus.eu/user/g/g2ssmee/imas2xarray/data')

dataset = handle.get_variables(variables=(x_var, y_var, time_var))
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Collection

import h5py
import numpy as np
import xarray as xr

from ._lookup import var_lookup
from ._rebase import squash_placeholders

if TYPE_CHECKING:
    from ._models import IDSVariableModel


class EmptyVarError(Exception):
    ...


class MissingVarError(Exception):
    ...


def _var_path_to_hdf5_key_and_slices(path: str) -> tuple[str, tuple[slice | int, ...]]:
    """Deconstruct variable path into HDF5 key and slice operators.

    Parameters
    ----------
    path : str
        Path from `IDSVariableModel`

    Returns
    -------
    tuple[str, list[slice]]
        IMAS compatible path and data slicers
    """
    key_parts: list[str] = []
    slices: list[slice | int] = []

    delimiter = '&'
    array_symbol = '[]'

    for part in path.split('/'):
        if part == '*':
            slices.append(slice(None))
            key_parts[-1] += array_symbol
        elif part.isdigit():
            index = int(part)
            slices.append(index)
            key_parts[-1] += array_symbol
        else:
            key_parts.append(part)

    key = delimiter.join(key_parts)

    return key, tuple(slices)


def _mapping_to_xarray(
    data_file: h5py.File,
    variables: Collection[str | IDSVariableModel],
    missing_ok: bool = False,
    empty_ok: bool = False,
) -> xr.Dataset:
    """Return dataset for given variables.

    Parameters
    ----------
    data_file : h5py.File
        Open hdf5 file
    variables : Collection[str | IDSVariableModel]]
        List of data variables
    missing_ok : bool
        Ignore missing variables from dataset
    empty_ok : bool
        Add empty fields to output

    Returns
    -------
    ds : xr.Dataset
        Return query as Dataset
    """
    xr_data_vars: dict[str, tuple[list[str], np.ndarray]] = {}

    variables = var_lookup.lookup(variables)

    for var in variables:
        key, slices = _var_path_to_hdf5_key_and_slices(var.path)

        if key not in data_file:
            if missing_ok:
                continue
            raise MissingVarError(
                f'{var.path} does not exist in data file (HDF5 key: {key!r}) .'
            )

        arr = data_file[key]

        if (not empty_ok) and (arr.size == 0):
            raise EmptyVarError(f'Variable {var.name!r} contains empty data.')

        if len(slices) == 0:
            xr_data_vars[var.name] = (var.dims, arr)
        else:
            xr_data_vars[var.name] = ([*var.dims], arr[slices])

    ds = xr.Dataset(data_vars=xr_data_vars)

    return ds


def to_xarray(
    path: str | Path, *, ids: str, variables: None | Collection[str] = None
) -> xr.Dataset:
    """Load IDS from given path to IMAS data into an xarray dataset.

    IMAS data must be in HDF5 format.

    Parameters
    ----------
    path : str | Path
        Path to the data
    ids : str
        The IDS to load (i.e. 'core_profiles')
    variables : None | list[str], optional
        List of variables to load. If None, attempt to load
        all variables known to `imas2xarray`

    Returns
    -------
    dataset : xr.Dataset
        Xarray dataset with all specified variables
    """
    h = H5Handle(path)

    if variables:
        return h.get_variables(variables=variables, ids=ids)
    else:
        return h.get_all_variables(ids=ids)


def to_imas(
    path: str | Path, dataset: xr.Dataset, *, ids: str, variables: None | Collection[str] = None
):
    """Write variables in xarray dataset back to IMAS data at given path.

    Update only, IMAS data must be in HDF5 format.

    Parameters
    ----------
    path : str | Path
        Path to the data
    dataset : xr.Dataset
        Input dataset
    ids : str
        The IDS to write to (i.e. 'core_profiles')
    variables : Collection[str]
        List of variables to write back. If None, attempt to write back
        all variables known to `imas2xarray`
    """
    h = H5Handle(path)

    h.set_variables(dataset, ids=ids, variables=variables)


class H5Handle:
    def __init__(self, path: Path | str):
        self.path = Path(path)

    @contextmanager
    def open_ids(self, ids: str = 'core_profiles', mode='r') -> h5py.File:
        """Context manager to open the IDS file.

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

        with h5py.File(data_file, mode) as f:
            yield f[ids]

    def get_all_variables(
        self,
        *,
        ids: str,
        extra_variables: None | Collection[IDSVariableModel] = None,
        squash: bool = True,
        **kwargs,
    ) -> xr.Dataset:
        """Get all known variables from selected ids from the dataset.

        This function looks up the data location from the
        `imas2xarray.var_lookup` table

        Parameters
        ----------
        ids : str
            The IDS to write to (i.e. 'core_profiles')
        extra_variables : Collection[IDSVariableModel]
            Extra variables to load in addition to the ones known through the config
        squash : bool
            Squash placeholder variables
        **kwargs
            These keyword arguments are passed to `H5Handle.to_xarray()`

        Returns
        -------
        ds : xarray
            The data in `xarray` format.
        """
        extra_variables = extra_variables or []

        idsvar_lookup = var_lookup.filter_ids(ids)
        variables = list(set(list(extra_variables) + list(idsvar_lookup.keys())))
        return self.get_variables(variables, ids=ids, squash=squash, missing_ok=True, **kwargs)

    def get_variables(
        self,
        variables: Collection[str | IDSVariableModel],
        *,
        ids: str,
        squash: bool = True,
        **kwargs,
    ) -> xr.Dataset:
        """Get variables from data set.

        This function looks up the data location from the
        `imas2xarray.var_lookup` table, and returns

        Parameters
        ----------
        variables : Collection[Union[str, IDSVariableModel]]
            Variable names of the data to load.
        ids : str
            The IDS to write to (i.e. 'core_profiles')
        squash : bool
            Squash placeholder variables
        **kwargs
            These keyword arguments are passed to `IDSMapping.to_xarray()`

        Returns
        -------
        ds : xarray
            The data in `xarray` format.

        Raises
        ------
        ValueError
            When variables are from different IDS.
        """
        var_models = var_lookup.lookup(variables)

        for var in var_models:
            if var.ids != ids:
                raise ValueError(f'Variable {var} does not belong to {ids}.')

        with self.open_ids(ids, 'r') as group:
            ds = _mapping_to_xarray(group, variables=var_models, **kwargs)

        if squash:
            ds = squash_placeholders(ds)

        return ds

    def set_variables(
        self, dataset: xr.Dataset, *, ids: str, variables: None | Collection[str] = None
    ):
        """Update variables in corresponding ids datafile.

        Parameters
        ----------
        dataset : xr.Dataset
            Dataset with variables to write. Their dimensions must match those of the
            target dataset.
        ids : str
            IDS to write to.
        variables : Collection[str], optional
            List of data variables to write.
        """
        if not variables:
            variables = list(dataset.variables)
            # TODO: check variables in var_lookup

        var_models = var_lookup.lookup(variables)

        for var in var_models:
            if var.ids != ids:
                raise ValueError(f'Variable {var} does not belong to {ids}.')

        with self.open_ids(ids, 'r+') as group:
            for var in var_models:
                arr = dataset[var.name]

                key, slices = _var_path_to_hdf5_key_and_slices(var.path)

                group[key][slices] = arr
