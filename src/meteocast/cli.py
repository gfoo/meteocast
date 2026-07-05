"""Interface en ligne de commande de meteocast."""

from __future__ import annotations

import typer

from meteocast import __version__
from meteocast.client import get_current, get_forecast
from meteocast.errors import MeteocastError
from meteocast.providers import DEFAULT_SOURCE

app = typer.Typer(
    name="meteocast",
    help="Récupère des informations météo et des prévisions.",
    no_args_is_help=True,
    add_completion=False,
)

_SOURCE_OPTION = typer.Option(DEFAULT_SOURCE, "--source", "-s", help="Source météo à utiliser.")


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
def current(
    location: str = typer.Argument(..., help="Localité (ville, code postal…)."),
    source: str = _SOURCE_OPTION,
) -> None:
    """Affiche la météo courante pour une localité."""
    try:
        weather = get_current(location, source=source)
    except (MeteocastError, ValueError) as exc:
        typer.secho(f"⚠️  {exc}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(f"{weather.location} : {weather.temperature_c} °C, {weather.description}")


@app.command()
def forecast(
    location: str = typer.Argument(..., help="Localité (ville, code postal…)."),
    days: int = typer.Option(3, "--days", "-d", min=1, max=16, help="Nombre de jours."),
    source: str = _SOURCE_OPTION,
) -> None:
    """Affiche la prévision sur plusieurs jours pour une localité."""
    try:
        result = get_forecast(location, days=days, source=source)
    except (MeteocastError, ValueError) as exc:
        typer.secho(f"⚠️  {exc}", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(f"Prévision sur {days} jours pour {result.location}")
    for day in result.daily:
        typer.echo(
            f"  {day.date} : {day.temperature_min_c} – {day.temperature_max_c} °C"
            f" — {day.description}"
        )


def main() -> None:
    """Point d'entrée console (référencé par ``[project.scripts]``)."""
    app()


if __name__ == "__main__":
    main()
