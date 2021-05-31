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
    config = providers.Configuration(
        default={
            "service": {"addr": "127.0.0.1", "port": 1234, "api_key": "default:key"},
            "plugins": {"paths": {}},
        }
    )

    user_dirs: providers.Provider[UserDirPaths] = providers.Dependency(UserDirPaths)  # type: ignore

    wksp_dirs: providers.Provider[WorkspaceDirPaths] = providers.Dependency(
        WorkspaceDirPaths
    )

    service: providers.Singleton[MyService] = providers.Singleton(
        MyService, config.service.addr, config.service.port, config.service.api_key
    )
