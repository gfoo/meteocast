"""Interface en ligne de commande de meteocast."""

from __future__ import annotations

import typer

from meteocast import __version__
from meteocast.client import get_current, get_forecast

app = typer.Typer(
    name="meteocast",
    help="Récupère des informations météo et des prévisions.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"meteocast {__version__}")
        raise typer.Exit()


@app.callback()
def _main(
    _version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Affiche la version et quitte.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """meteocast — météo et prévisions en ligne de commande."""


@app.command()
def current(location: str = typer.Argument(..., help="Localité (ville, code postal…).")) -> None:
    """Affiche la météo courante pour une localité."""
    try:
        weather = get_current(location)
    except NotImplementedError as exc:
        typer.secho(f"⚠️  {exc}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(f"{weather.location}: {weather.temperature_c} °C, {weather.description}")


@app.command()
def forecast(
    location: str = typer.Argument(..., help="Localité (ville, code postal…)."),
    days: int = typer.Option(3, "--days", "-d", min=1, max=16, help="Nombre de jours."),
) -> None:
    """Affiche la prévision sur plusieurs jours pour une localité."""
    try:
        result = get_forecast(location, days=days)
    except NotImplementedError as exc:
        typer.secho(f"⚠️  {exc}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(f"Prévision sur {days} jours pour {result.location}")
    for day in result.daily:
        typer.echo(f"  {day.temperature_c} °C — {day.description}")


def main() -> None:
    """Point d'entrée console (référencé par ``[project.scripts]``)."""
    app()


if __name__ == "__main__":
    main()
