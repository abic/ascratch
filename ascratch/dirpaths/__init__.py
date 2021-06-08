"""A Common directory paths lookup for various platforms and workspaces.

Where do configs go?
Where do logs go?
Where does user data get written?

This module should be a generic way to answer all those questions.
"""

from .platform import UserDirPaths
from .workspace import WorkspaceDirPaths

import sys

from pathlib import Path


def user(name: str) -> UserDirPaths:
    return UserDirPaths(name)


def workspace(root: Path) -> WorkspaceDirPaths:
    return WorkspaceDirPaths(root)


__all__ = ("UserDirPaths", "WorkspaceDirPaths", "user")
