"""Dir paths for systems that use the XDG Base Directory Specification.

See: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""

from pathlib import Path

from .platform import UserDirPaths

class XDGDirPaths(UserDirPaths):
    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def config(self) -> Path:
        return Path.home() / ".config" / self._name

    @property
    def data(self) -> Path:
        return Path.home() / ".local" / "share" / self._name

    @property
    def cache(self) -> Path:
        return Path.home() / ".cache" / self._name
