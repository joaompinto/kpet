import typer

from .cli import ctx, get, main, show


def app_main():
    app = typer.Typer(short_help="Cool")

    app.callback()(main.main)
    app.command()(ctx.ctx)
    app.command()(get.get)
    app.command()(show.show)
    app()


if __name__ == "__main__":
    app_main()
