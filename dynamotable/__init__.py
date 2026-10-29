"""Read and write Dynamo tables as pandas dataframes."""

from importlib.metadata import PackageNotFoundError, version

from .io import read, write

try:
    __version__ = version("dynamotable")
except PackageNotFoundError:
    __version__ = "uninstalled"


__all__ = ["read", "write"]
