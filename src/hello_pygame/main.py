import sys

import typer
from py_app_dev.core.exceptions import UserNotificationException
from py_app_dev.core.logging import logger, setup_logger, time_it

from hello_pygame import __version__
from hello_pygame.my_game import MyGame

package_name = "hello_pygame"

app = typer.Typer(name=package_name, help="Playground for PyGame", no_args_is_help=True, add_completion=False)


@app.callback(invoke_without_command=True)
def version(
    version: bool = typer.Option(None, "--version", "-v", is_eager=True, help="Show version and exit."),
) -> None:
    if version:
        typer.echo(f"{package_name} {__version__}")
        raise typer.Exit()


@app.command()
@time_it("run")
def run() -> None:
    MyGame().run()


def main() -> int:
    try:
        setup_logger()
        app()
        return 0
    except UserNotificationException as e:
        logger.error(f"{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
