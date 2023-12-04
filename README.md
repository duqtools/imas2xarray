[![Documentation Status](https://readthedocs.org/projects/imas2xarray/badge/?version=latest)](https://imas2xarray.readthedocs.io/en/latest/?badge=latest)
[![Tests](https://github.com/duqtools/imas2xarray/actions/workflows/test.yaml/badge.svg)](https://github.com/duqtools/imas2xarray/actions/workflows/test.yaml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/imas2xarray)](https://pypi.org/project/imas2xarray/)
[![PyPI](https://img.shields.io/pypi/v/imas2xarray.svg?style=flat)](https://pypi.org/project/imas2xarray/)
![Coverage](https://gist.githubusercontent.com/stefsmeets/f635ee4ac999ce969fa1d23a57e006ae/raw/covbadge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10256040.svg)](https://doi.org/10.5281/zenodo.10256040)

![imas2xarray banner](https://raw.githubusercontent.com/duqtools/imas2xarray/main/src/imas2xarray/data/logo.png)


# imas2xarray

**Imas2xarray** is a library that makes it as simple and intuitive as possible to load an IMAS dataset in HDF5 format into Python. There is no need to manually define the paths or fiddle with the different dimensions and long keys.

```python
>>> from imas2xarray import to_xarray
>>>
>>> path = '/pfs/work/g2aho/public/imasdb/test/3/92436/1/'
>>> ids = 'equilibrium'
>>>
>>> ds = to_xarray(path, ids)
>>> ds
<xarray.Dataset>
Dimensions:         (time: 1, rho_tor_norm: 101, ion: 4)
Coordinates:
  * time            (time) float64 50.04
  * rho_tor_norm    (rho_tor_norm) float64 0.0 0.01 0.02 0.03 ... 0.98 0.99 1.0
Dimensions without coordinates: ion
Data variables: (12/14)
    q               (time, rho_tor_norm) float64 0.7887 0.7888 ... 4.262 4.845
    collisionality  (time, rho_tor_norm) float64 23.23 7.554 ... 7.31 10.19
    t_i_ave         (time, rho_tor_norm) float64 1.036e+04 1.036e+04 ... 508.4
    ...              ...
    n_e             (time, rho_tor_norm) float64 7.976e+19 ... 1.742e+19
    p_i             (time, ion, rho_tor_norm) float64 1.242e+05 ... 0.2948
    n_e_tot         (time, rho_tor_norm) float64 7.976e+19 ... 1.742e+19
```

For more advanced use-cases and examples, please see the [documentation](https://imas2xarray.readthedocs.io).

## Installing imas2xarray

To install:

```console
pip install imas2xarray
```

Imas2xarray is supported on Python versions 3.9 or newer.

## Development

Check out our [Contributing Guidelines](CONTRIBUTING.md#Getting-started-with-development) to get started with development.

Suggestions, improvements, and edits are most welcome.
