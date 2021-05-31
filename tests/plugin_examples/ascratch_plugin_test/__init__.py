from typing import Optional
from ascratch.plugins import CommandPlugin, register
import click

import sys

class Foo(CommandPlugin):
    def name(self) -> str:
        return "foo"

    def list_commands(self) -> str:
        return "foobar"
    
    def get_command(self, name: str) -> Optional[click.Command]:
        if name != "foobar":
            return None
        
        return None
        

register(Foo())
