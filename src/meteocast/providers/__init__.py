"""Registre des fournisseurs météo.

Deux registres distincts (météo courante / prévision) : un fournisseur peut
implémenter l'un, l'autre, ou les deux. Ajouter une source revient à écrire une
classe conforme au protocole correspondant puis à l'enregistrer ici (ou via
``register_current`` / ``register_forecast``).
"""

from __future__ import annotations

from meteocast.providers.base import CurrentProvider, ForecastProvider
from meteocast.providers.openmeteo import OpenMeteoProvider

DEFAULT_SOURCE = "open-meteo"

_openmeteo = OpenMeteoProvider()

_CURRENT_PROVIDERS: dict[str, CurrentProvider] = {_openmeteo.name: _openmeteo}
_FORECAST_PROVIDERS: dict[str, ForecastProvider] = {_openmeteo.name: _openmeteo}


def available_sources() -> list[str]:
    """Liste triée des sources disponibles (courant ∪ prévision)."""
    return sorted(set(_CURRENT_PROVIDERS) | set(_FORECAST_PROVIDERS))


def register_current(provider: CurrentProvider) -> None:
    """Enregistre un fournisseur de météo courante sous son ``name``."""
    _CURRENT_PROVIDERS[provider.name] = provider


def register_forecast(provider: ForecastProvider) -> None:
    """Enregistre un fournisseur de prévision sous son ``name``."""
    _FORECAST_PROVIDERS[provider.name] = provider


def get_current_provider(source: str) -> CurrentProvider:
    try:
        return _CURRENT_PROVIDERS[source]
    except KeyError:
        raise ValueError(
            f"Source de météo courante inconnue : {source!r}. "
            f"Disponibles : {', '.join(sorted(_CURRENT_PROVIDERS))}."
        ) from None


def get_forecast_provider(source: str) -> ForecastProvider:
    try:
        return _FORECAST_PROVIDERS[source]
    except KeyError:
        raise ValueError(
            f"Source de prévision inconnue : {source!r}. "
            f"Disponibles : {', '.join(sorted(_FORECAST_PROVIDERS))}."
        ) from None


__all__ = [
    "CurrentProvider",
    "ForecastProvider",
    "OpenMeteoProvider",
    "DEFAULT_SOURCE",
    "available_sources",
    "register_current",
    "register_forecast",
    "get_current_provider",
    "get_forecast_provider",
]
