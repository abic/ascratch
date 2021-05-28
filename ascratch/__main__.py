#!/usr/bin/env python3

import argparse
import asyncio
import click
import sys
import toml

from pathlib import Path
from . import TOOLNAME, ToolContainer, MyService, dirpaths

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


class MyCLI(click.MultiCommand):
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


def _default_config(config: providers.Configuration) -> None:
    config.from_dict(
        {"service": {"addr": "127.0.0.1", "port": 1234, "api_key": "default:key",}}
    )


def _options_config(
    config: providers.Configuration, options: argparse.Namespace
) -> None:
    options_config: Dict[str, Any] = {}

    if options.api_key is not None:
        options_config.setdefault("service", {})["api_key"] = options.api_key

    config.from_dict(options_config)


def _toml_config(config: providers.Configuration, config_path: Path) -> None:
    try:
        config.from_dict(dict(toml.load(config_path)))
    except FileNotFoundError:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(prog=TOOLNAME)

    parser.add_argument(
        "-k", "--api-key",
    )

    parser.add_argument("-c", "--config", type=Path)

    options: argparse.Namespace = parser.parse_args()

    wksp_dirs = dirpaths.workspace(_find_root())
    user_dirs = dirpaths.user(TOOLNAME)

    tool = ToolContainer(wksp_dirs=wksp_dirs, user_dirs=user_dirs)

    _default_config(tool.config)
    _toml_config(tool.config, user_dirs.config / "config.toml")
    _toml_config(tool.config, wksp_dirs.config / "config.toml")
    if options.config is not None:
        _toml_config(tool.config, options.config)
    _options_config(tool.config, options)

    tool.wire(modules=[sys.modules[__name__]])

    asyncio.run(run())


if __name__ == "__main__":
    main()
