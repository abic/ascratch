"""Dir paths for a managed workspace.
"""

from pathlib import Path


class WorkspaceDirPaths:

    _root: Path

    def __init__(self, root: Path) -> None:
        self._root = root

    @property
    def root(self) -> Path:
        return self._root

    @property
    def config(self) -> Path:
        return self._root / ".config"

    @property
    def data(self) -> Path:
        return self._root / ".data"

    @property
    def cache(self) -> Path:
        return self._root / ".cache"
