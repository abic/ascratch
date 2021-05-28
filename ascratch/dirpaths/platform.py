"""Interfaces that platform specific dirpaths should implement
"""

from abc import ABC, abstractmethod
from pathlib import Path

class UserDirPaths(ABC):

    @property
    @abstractmethod
    def config(self) -> Path:
        ...

    @property
    @abstractmethod
    def data(self) -> Path:
        ...

    @property
    @abstractmethod
    def cache(self) -> Path:
        ...
