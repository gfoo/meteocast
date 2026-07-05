"""Tests de la CLI et de la validation de haut niveau."""

import pytest
from typer.testing import CliRunner

from meteocast import __version__
from meteocast.cli import app
from meteocast.client import get_current, get_forecast
from meteocast.models import DayForecast, Forecast, Weather
from meteocast.providers import register_current, register_forecast

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_help_lists_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "current" in result.stdout
    assert "forecast" in result.stdout


# --- Validation des entrées (aucun accès réseau) -----------------------------


def test_get_forecast_rejects_empty_location() -> None:
    with pytest.raises(ValueError):
        get_forecast("")


def test_get_forecast_rejects_out_of_range_days() -> None:
    with pytest.raises(ValueError):
        get_forecast("Lausanne", days=99)


def test_get_current_rejects_empty_location() -> None:
    with pytest.raises(ValueError):
        get_current("")


def test_unknown_source_raises() -> None:
    with pytest.raises(ValueError):
        get_current("Lausanne", source="inexistant")


# --- CLI câblée à un fournisseur factice (via le registre) -------------------


class _StubProvider:
    """Fournisseur de test conforme aux deux protocoles."""

    name = "stub"

    def get_current(self, location: str, *, timeout: float) -> Weather:
        return Weather(location="Testville", temperature_c=20.0, description="Ciel dégagé")

    def get_forecast(self, location: str, *, days: int, timeout: float) -> Forecast:
        return Forecast(
            location="Testville",
            daily=[DayForecast("2026-07-05", 12.0, 22.0, "Ciel dégagé")],
        )


_stub = _StubProvider()
register_current(_stub)
register_forecast(_stub)


def test_cli_current_with_stub_source() -> None:
    result = runner.invoke(app, ["current", "Testville", "--source", "stub"])
    assert result.exit_code == 0
    assert "Testville" in result.stdout
    assert "20.0" in result.stdout


def test_cli_forecast_with_stub_source() -> None:
    result = runner.invoke(app, ["forecast", "Testville", "--source", "stub", "--days", "1"])
    assert result.exit_code == 0
    assert "Testville" in result.stdout
    assert "Ciel dégagé" in result.stdout


def test_cli_unknown_source_exits_2() -> None:
    result = runner.invoke(app, ["current", "Lausanne", "--source", "nope"])
    assert result.exit_code == 2
