#!/usr/bin/env python3

import asyncio
import click
import sys
import toml

from dependency_injector import providers
from dependency_injector.wiring import inject, Provide
from pathlib import Path
from typing import Dict

from . import dirpaths, plugins
from .cli import CLI
from .container import ToolContainer
from .service import MyService
from ascratch import cli


@inject
async def run(
    service: MyService = Provide[ToolContainer.service],
    wksp_dirs: dirpaths.WorkspaceDirPaths = Provide[ToolContainer.wksp_dirs],
    user_dirs: dirpaths.UserDirPaths = Provide[ToolContainer.user_dirs],
) -> None:
    print(service)
    print(wksp_dirs.config)
    print(user_dirs.config)


def _find_root() -> Path:
    dir = Path(__file__).parent.absolute()

    while not dir.joinpath(".git").exists():
        dir = dir.parent
        if dir == dir.root:
            raise RuntimeError("Not in ascratch git repo")
    return dir


def _toml_config(config: providers.Configuration, config_path: Path) -> None:
    try:
        config.from_dict(dict(toml.load(config_path)))
    except FileNotFoundError:
        pass


TOOLNAME: str = "ascratch"


@click.group()
def main() -> None:
    ...


@main.command()
def example() -> None:
    asyncio.run(run())


def _init() -> None:
    wksp_dirs = dirpaths.workspace(_find_root())
    user_dirs = dirpaths.user(TOOLNAME)

    tool = ToolContainer(wksp_dirs=wksp_dirs, user_dirs=user_dirs)

    _toml_config(tool.config, user_dirs.config / "config.toml")
    _toml_config(tool.config, wksp_dirs.config / "config.toml")

    plugin_paths = [
        path.replace("%workspacedir%", str(wksp_dirs.root))
        for path in tool.config.plugins.paths().values()
    ]

    plugins.load_plugins(plugin_paths)

    tool.wire(modules=[sys.modules[__name__]])

    for cmd_plugin in plugins.get(plugins.CommandPlugin):  # type: ignore
        for name in cmd_plugin.list_commands():
            cmd = cmd_plugin.get_command(name)
            if cmd is None:
                continue
            main.add_command(cmd)
    main.context_settings
    main()


if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
    except ModuleNotFoundError:
        # gracefully proceed when uvloop can't be loaded
        pass
    _init()
