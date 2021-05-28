#!/usr/bin/env python3

import argparse
from ascratch.dirpaths import workspace
import asyncio
import click
import sys
import toml

from pathlib import Path
from . import TOOLNAME, ToolContainer, MyService, dirpaths

from typing import List, Optional

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


def main() -> None:
    parser = argparse.ArgumentParser(prog=TOOLNAME)

    options = parser.parse_args()

    wksp_dirs = dirpaths.workspace(_find_root())
    user_dirs = dirpaths.user(TOOLNAME)

    tool = ToolContainer(wksp_dirs=wksp_dirs, user_dirs=user_dirs)

    try:
        tool.config.from_dict(dict(toml.load(user_dirs.config / "config.toml")))
    except FileNotFoundError:
        pass

    try:
        tool.config.from_dict(dict(toml.load(wksp_dirs.config / "config.toml")))
    except FileNotFoundError:
        pass

    tool.wire(modules=[sys.modules[__name__]])

    asyncio.run(run())


if __name__ == "__main__":
    main()
