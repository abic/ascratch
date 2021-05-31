import click

from typing import Any, Dict, List, Optional


class CLI(click.MultiCommand):

    _commands: Dict[str, click.Command]

    def __init__(
        self, name: str, commands: Dict[str, click.Command], **attrs: Any
    ) -> None:
        super().__init__(name, **attrs)
        self._commands = commands

    def list_commands(self, ctx: click.Context) -> List[str]:
        return sorted(self._commands.keys())

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        return self._commands.get(name)
