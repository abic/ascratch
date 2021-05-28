#!/usr/bin/env python3

import argparse
import asyncio
import sys
import toml

from pathlib import Path
from . import ToolContainer, MyService

from dependency_injector.wiring import inject, Provide


@inject
async def run(service: MyService = Provide[ToolContainer.service]) -> None:
    print(service)


def main() -> None:
    parser = argparse.ArgumentParser(prog="ascratch")

    options = parser.parse_args()

    tool = ToolContainer()
    config_path = Path.home().joinpath(".config/ascratch/config.toml")
    try:
        tool.config.from_dict(dict(toml.load(config_path)))
    except FileNotFoundError:
        pass

    tool.wire(modules=[sys.modules[__name__]])

    asyncio.run(run())


if __name__ == "__main__":
    main()
