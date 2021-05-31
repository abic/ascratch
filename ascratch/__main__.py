#!/usr/bin/env python3

import argparse
import asyncio
import click
import sys
import toml

from pathlib import Path
from . import TOOLNAME, ToolContainer, MyService, dirpaths, plugins


from typing import Any, Dict, List, Optional

from dependency_injector import providers
from dependency_injector.wiring import inject, Provide


@inject
async def run(
    service: MyService = Provide[ToolContainer.service],
    wksp_dirs: dirpaths.WorkspaceDirPaths = Provide[ToolContainer.wksp_dirs],
    user_dirs: dirpaths.UserDirPaths = Provide[ToolContainer.user_dirs],
) -> None:
    print(service)
    print(wksp_dirs.config)
    print(user_dirs.config)


class CLI(click.MultiCommand):
    def list_commands(self, ctx: click.Context) -> List[str]:
        return []

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        return None


def _find_root() -> Path:
    dir = Path(__file__).parent.absolute()

    while not dir.joinpath(".git").exists():
        dir = dir.parent
        if dir == dir.root:
            raise RuntimeError("Not in ascratch git repo")
    return dir


def _options_config(config: providers.Configuration, api_key: Optional[str]) -> None:
    if api_key is not None:
        config.set("service.api_key", api_key)


def _toml_config(config: providers.Configuration, config_path: Path) -> None:
    try:
        config.from_dict(dict(toml.load(config_path)))
    except FileNotFoundError:
        pass

@click.group(TOOLNAME, invoke_without_command=True)
def main() -> None:
    asyncio.run(run())



def _bootstrap(api_key: Optional[str] = None, config: Optional[Path] = None) -> None:
    wksp_dirs = dirpaths.workspace(_find_root())
    user_dirs = dirpaths.user(TOOLNAME)

    tool = ToolContainer(wksp_dirs=wksp_dirs, user_dirs=user_dirs)

    _toml_config(tool.config, user_dirs.config / "config.toml")
    _toml_config(tool.config, wksp_dirs.config / "config.toml")
    _options_config(tool.config, api_key)

    plugin_paths = [
        path.replace("%workspacedir%", str(wksp_dirs.root))
        for path in tool.config.plugins.paths().values()
    ]

    plugins.load_plugins(plugin_paths)

    tool.wire(modules=[sys.modules[__name__]])
    main()


if __name__ == "__main__":
    _bootstrap()
