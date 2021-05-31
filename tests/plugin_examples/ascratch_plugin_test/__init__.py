import click

from ascratch.plugins import commands, register


@click.command()
def test() -> None:
    click.echo("from plugin")

register(commands("test", test))
