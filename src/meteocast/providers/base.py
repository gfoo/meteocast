"""Abstractions de fournisseurs météo.

Deux contrats *distincts* — un pour la météo courante, un pour la prévision —
afin de pouvoir brancher indépendamment un nouveau fournisseur de l'un ou de
l'autre. Un même fournisseur peut implémenter les deux (comme Open-Meteo), un
seul, ou n'importe quelle combinaison.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from meteocast.models import Forecast, Weather


@runtime_checkable
class CurrentProvider(Protocol):
    """Fournit la météo courante pour une localité."""

    name: str

    def get_current(self, location: str, *, timeout: float) -> Weather: ...


@runtime_checkable
class ForecastProvider(Protocol):
    """Fournit une prévision sur plusieurs jours pour une localité."""

    name: str

    def get_forecast(self, location: str, *, days: int, timeout: float) -> Forecast: ...
