# Examples

## Modify data

Below is an example of how to use **imas2xarray** to data in-place.

Note that **Imas2xarray** can only update data in-place, i.e. the new data must have the same shape as the existing data.

```python
{!../scripts/modify_data.py!}
```

[Source code](https://github.com/duqtools/imas2xarray/tree/main/scripts/modify_data.py)

## Plotting single dataset

Below is an example of how to use **imas2xarray** to plot data with [matplotlib](https://matplotlib.org/).

```python
{!../scripts/plot_with_matplotlib.py!}
```

[Source code](https://github.com/duqtools/imas2xarray/tree/main/scripts/plot_with_matplotlib.py)

## Plotting multiple datasets

The code below shows how to make a plot with [matplotlib](https://matplotlib.org/) for multiple datasets.

For a more advanced example of how to concatenate data, check out the [example notebooks](./notebooks/xarray.ipynb).

```python
{!../scripts/plot_with_matplotlib_multi.py!}
```

[Source code](https://github.com/duqtools/imas2xarray/tree/main/scripts/plot_with_matplotlib_multi.py)
