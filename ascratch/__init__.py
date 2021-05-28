from dependency_injector import containers, providers

from typing import NamedTuple


class MyService(NamedTuple):
    addr: str
    port: int


class ToolContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    service = providers.Singleton(MyService, config.service.addr, config.service.port)
