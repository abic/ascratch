from typing import List, Optional
from ascratch.plugins import CommandPlugin, register
import click

import sys

@click.command()
def test() -> None:
    click.echo("from plugin")

class Foo(CommandPlugin):
    @property
    def name(self) -> str:
        return "foo"

    def list_commands(self) -> List[str]:
        return ["foobar"]
    
    def get_command(self, name: str) -> Optional[click.Command]:
        if name != "foobar":
            return None
        
        return None
        

register(Foo())
