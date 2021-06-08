"""Interfaces that platform specific dirpaths should implement
"""

import appdirs
from pathlib import Path

class UserDirPaths:
    _appdirs: appdirs.AppDirs

    def __init__(self, name: str) -> None:
        self._appdirs = appdirs.AppDirs(appname=name, appauthor=False)

    @property
    def config(self) -> Path:
        return Path(self._appdirs.user_config_dir)

    @property
    def data(self) -> Path:
        return Path(self._appdirs.user_data_dir)

    @property
    def cache(self) -> Path:
        return Path(self._appdirs.user_cache_dir)
