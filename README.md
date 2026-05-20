## GRIB2 Backend Selection

Kerchunk supports two mutually exclusive backends for GRIB2 file processing: `grib2io` and `cfgrib` (with eccodes). The backend is selected at runtime using the environment variable `KERCHUNK_GRIB_ENGINE`.

- Set `KERCHUNK_GRIB_ENGINE=grib2io` to use the [grib2io](https://github.com/jswhit/grib2io) backend (recommended for pure Python, no eccodes/cfgrib dependency).
- Set `KERCHUNK_GRIB_ENGINE=cfgrib` to use the [cfgrib](https://github.com/ecmwf/cfgrib) backend (requires eccodes and cfgrib).
- If the variable is unset or invalid, the default is `cfgrib`.

**Only the selected backend is imported and used.** If you choose `grib2io`, you do not need to install eccodes or cfgrib. If you choose `cfgrib`, you do not need grib2io.

Example usage:

```bash
export KERCHUNK_GRIB_ENGINE=grib2io
python -m pytest tests/test_grib.py
```

See the documentation for more details on backend-specific requirements and behavior.
# kerchunk

Cloud-friendly access to archival data

[![Docs](https://github.com/fsspec/kerchunk/actions/workflows/default.yml/badge.svg)](https://fsspec.github.io/kerchunk/)
[![Tests](https://github.com/fsspec/kerchunk/actions/workflows/tests.yml/badge.svg)](https://github.com/fsspec/kerchunk/actions/workflows/tests.yml)
[![Pypi](https://img.shields.io/pypi/v/kerchunk.svg)](https://pypi.python.org/pypi/kerchunk/)
[![Conda-forge](https://img.shields.io/conda/vn/conda-forge/kerchunk.svg)](https://anaconda.org/conda-forge/kerchunk)

Kerchunk is a library that provides a unified way to represent a variety of chunked, compressed
data formats (e.g. NetCDF, HDF5, GRIB),
allowing efficient access to the data from traditional file systems or cloud object storage.
It also provides a flexible way to create
virtual datasets from multiple files.  It does this by extracting the byte ranges,
compression information and other information about the
data and storing this metadata in a new, separate object.  This means that you can
create a virtual aggregate dataset over potentially many source
files, for efficient, parallel and cloud-friendly *in-situ* access without having to copy or
translate the originals. It is a gateway to in-the-cloud massive data processing while
the data providers still insist on using legacy formats for archival storage.

*Why Kerchunk*:

We provide the following things:

- completely serverless architecture
- metadata consolidation, so you can understand a many-file dataset (metadata plus physical storage) in a single read
- read from all of the storage backends supported by fsspec, including object storage (s3, gcs, abfs, alibaba), http,
  cloud user storage (dropbox, gdrive) and network protocols (ftp, ssh, hdfs, smb...)
- loading of various file types (currently netcdf4/HDF, grib2, tiff, fits, zarr), potentially heterogeneous within a
  single dataset, without a need to go via the specific driver (e.g., no need for h5py)
- asynchronous concurrent fetch of many data chunks in one go, amortizing the cost of latency
- parallel access with a library like zarr without any locks
- logical datasets viewing many (>~millions) data files, and direct access/subselection to them via coordinate
  indexing across an arbitrary number of dimensions


<img alt="logo" src="./kerchunk.png" width="200"/>


For further information, please see [the documentation](https://fsspec.github.io/kerchunk/).
