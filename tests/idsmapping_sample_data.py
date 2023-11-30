from __future__ import annotations

import numpy as np


class nested_val:
    val = np.array([123])


class profile_t0:
    grid = np.arange(10.0) * 1
    variable = grid**2
    val = 1
    empty = np.array([])


class profile_t1:
    grid = np.arange(10.0) * 2
    variable = grid**2
    val = 2
    empty = np.array([])


class profile_t2:
    grid = np.arange(10.0) * 3
    variable = grid**2
    val = 3
    empty = np.array([])


class ion_1:
    variable = np.arange(25.0).reshape(5, 5) * 1


class ion_2:
    variable = np.arange(25.0).reshape(5, 5) * 2


class ion_3:
    variable = np.arange(25.0).reshape(5, 5) * 3


class arr_t0:
    grid = np.arange(25.0).reshape(5, 5) * 1
    variable = grid**1
    ions = np.array([ion_1.variable, ion_2.variable, ion_3.variable])


class arr_t1:
    grid = np.arange(25.0).reshape(5, 5) * 2
    variable = grid**2
    ions = np.array([ion_1.variable, ion_2.variable, ion_3.variable])


class arr_t2:
    grid = np.arange(25.0).reshape(5, 5) * 3
    variable = grid**3
    ions = np.array([ion_1.variable, ion_2.variable, ion_3.variable])


arr = '[]'
delim = '&'

sample_data = {
    f'nested_profiles_1d{arr}{delim}data{delim}grid':
    np.stack([profile_t0.grid, profile_t1.grid, profile_t2.grid]),
    f'nested_profiles_1d{arr}{delim}data{delim}variable':
    np.stack([profile_t0.variable, profile_t1.variable, profile_t2.variable]),
    f'nested_profiles_2d{arr}{delim}data{delim}grid':
    np.stack([arr_t0.grid, arr_t1.grid, arr_t2.grid]),
    f'nested_profiles_2d{arr}{delim}data{delim}ions{arr}{delim}variable':
    np.stack([arr_t0.ions, arr_t1.ions, arr_t2.ions]),
    f'nested_profiles_2d{arr}{delim}data{delim}variable':
    np.stack([arr_t0.variable, arr_t1.variable, arr_t2.variable]),
    f'nested_single_profile_1d{delim}data{delim}grid':
    profile_t0.grid,
    f'nested_single_profile_1d{delim}data{delim}variable':
    profile_t0.variable,
    f'nested_single_profile_2d{delim}data{delim}grid':
    arr_t0.grid,
    f'nested_single_profile_2d{delim}data{delim}ions{arr}{delim}variable':
    arr_t0.ions,
    f'nested_single_profile_2d{delim}data{delim}variable':
    arr_t0.variable,
    f'nested_single_val{delim}val':
    nested_val.val,
    f'profiles_1d{arr}{delim}grid':
    np.stack([profile_t0.grid, profile_t1.grid, profile_t2.grid]),
    f'profiles_1d{arr}{delim}variable':
    np.stack([profile_t0.variable, profile_t1.variable, profile_t2.variable]),
    f'profiles_1d{arr}{delim}empty':
    np.stack([profile_t0.empty, profile_t1.empty, profile_t2.empty]),
    f'profiles_2d{arr}{delim}grid':
    np.stack([arr_t0.grid, arr_t1.grid, arr_t2.grid]),
    f'profiles_2d{arr}{delim}ions{arr}{delim}variable':
    np.stack([arr_t0.ions, arr_t1.ions, arr_t2.ions]),
    f'profiles_2d{arr}{delim}variable':
    np.stack([arr_t0.variable, arr_t1.variable, arr_t2.variable]),
    f'single_profile_1d{delim}grid':
    profile_t0.grid,
    f'single_profile_1d{delim}variable':
    profile_t0.variable,
    f'single_profile_2d{delim}grid':
    arr_t0.grid,
    f'single_profile_2d{delim}ions{arr}{delim}variable':
    arr_t0.ions,
    f'single_profile_2d{delim}variable':
    arr_t0.variable,
    'single_val':
    np.array([123]),
    'time':
    np.array((23, 24, 25)),
}
