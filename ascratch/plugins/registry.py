import importlib
import pkgutil
import site

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar
from types import ModuleType


class Plugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

PT = TypeVar("PT", bound=Plugin)

__plugins: Dict[Type[Any], List[Any]] = {}


def get(typ: Type[PT]) -> List[PT]:
    return __plugins.get(typ, [])


def register(plugin: Plugin) -> None:
    """Register a plugin instance.

    This will probably evolve into class + partial factor to support binding
    in the dependency injector.
    """

    if not isinstance(plugin, Plugin):
        raise RuntimeError("Plugin is not a Plugin: ", plugin)

    subclass = type(plugin)
    for clz in subclass.__mro__:
        if clz == Plugin:
            break
        subclass = clz
    if subclass == type(plugin):
        raise RuntimeError("Not a component plugin")

    __plugins.setdefault(subclass, []).append(plugin)


__discovered_plugin_modules: Optional[Dict[str, ModuleType]] = None


def load_plugins(path: Iterable[str]) -> None:
    global __discovered_plugin_modules
    modules = __discovered_plugin_modules
    if modules is not None:
        raise RuntimeError("plugins already loaded")

    for dir in path:
        site.addsitedir(dir)

    modules = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules(path)
        if name.startswith("ascratch_plugin_")
    }
    __discovered_plugin_modules = modules
