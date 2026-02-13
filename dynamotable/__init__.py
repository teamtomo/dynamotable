from importlib.metadata import PackageNotFoundError, version

from .io import read, write

try:
    __version__ = version("dynamotable")
except PackageNotFoundError:
    __version__ = "uninstalled"
