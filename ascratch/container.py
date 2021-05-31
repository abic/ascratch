from dependency_injector import containers, providers

from .dirpaths import WorkspaceDirPaths, UserDirPaths
from .service import MyService


class ToolContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        default={
            "service": {"addr": "127.0.0.1", "port": 1234, "api_key": "default:key"},
            "plugins": {"disabled": [], "namespace": {}, "paths": {}},
        }
    )

    user_dirs: providers.Provider[UserDirPaths] = providers.Dependency(UserDirPaths)  # type: ignore

    wksp_dirs: providers.Provider[WorkspaceDirPaths] = providers.Dependency(
        WorkspaceDirPaths
    )

    service: providers.Singleton[MyService] = providers.Singleton(
        MyService, config.service.addr, config.service.port, config.service.api_key
    )
