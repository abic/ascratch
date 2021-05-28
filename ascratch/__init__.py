from dependency_injector import containers, providers

from typing import NamedTuple

from pathlib import Path

from .dirpaths import WorkspaceDirPaths, UserDirPaths, user, workspace


class MyService(NamedTuple):
    addr: str
    port: int
    api_key: str


TOOLNAME: str = "ascratch"


class ToolContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Dirs will be overriden since they're neede to load configuration.
    user_dirs: providers.Singleton[UserDirPaths] = providers.Singleton(user, TOOLNAME)

    wksp_dirs: providers.Singleton[WorkspaceDirPaths] = providers.Singleton(
        workspace, Path(".").resolve()
    )

    service: providers.Singleton[MyService] = providers.Singleton(
        MyService, config.service.addr, config.service.port, config.service.api_key
    )
