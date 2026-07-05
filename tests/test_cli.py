"""Tests de l'interface en ligne de commande."""

import pytest
from typer.testing import CliRunner

from meteocast import __version__
from meteocast.cli import app
from meteocast.client import get_forecast

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


def test_forecast_not_implemented_yet() -> None:
    # Tant que l'API n'est pas branchée, la commande sort proprement en code 2.
    result = runner.invoke(app, ["forecast", "Lausanne"])
    assert result.exit_code == 2


def test_get_forecast_rejects_empty_location() -> None:
    with pytest.raises(ValueError):
        get_forecast("")


def test_get_forecast_rejects_out_of_range_days() -> None:
    with pytest.raises(ValueError):
        get_forecast("Lausanne", days=99)
