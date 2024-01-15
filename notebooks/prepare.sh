# Small script to initialize a few datasets for the notebooks using the `hdf5_testdata`:
# https://github.com/duqtools/hdf5_testdata/tree/main

git clone ~/python/hdf5_testdata 1
git clone ~/python/hdf5_testdata 2
git clone ~/python/hdf5_testdata 3

python prepare.py
