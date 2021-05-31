import click

from . import Plugin

from abc import abstractmethod
from typing import Dict, List, Optional

class CommandPlugin(Plugin):
    @abstractmethod
    def list_commands(self) -> List[str]:
        ...

    @abstractmethod
    def get_command(self, name: str) -> Optional[click.Command]:
        ...


class _CommandList(CommandPlugin):
    _name: str
    _commands: Dict[str, click.Command]

    def __init__(self, name: str, commands: Dict[str, click.Command]) -> None:
        self._name = name
        self._commands = commands

    @property
    def name(self) -> str:
        return self._name

    def list_commands(self) -> List[str]:
        return sorted(self._commands.keys())

    def get_command(self, name: str) -> Optional[click.Command]:
        return self._commands.get(name)


def commands(name: str, *cmds: click.Command) -> CommandPlugin:
    cmd_dict: Dict[str, click.Command] = {}
    for cmd in cmds:
        if cmd.name is None:
            raise RuntimeError("Command is nameless", cmd)
        cmd_dict[cmd.name] = cmd
    return _CommandList(name, cmd_dict)

