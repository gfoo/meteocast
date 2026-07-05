"""Modèles de données météo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Weather:
    """Conditions météo à un instant donné."""

    location: str
    temperature_c: float
    description: str


@dataclass(slots=True)
class DayForecast:
    """Prévision météo pour une journée."""

    date: str  # date ISO (AAAA-MM-JJ)
    temperature_min_c: float
    temperature_max_c: float
    description: str


@dataclass(slots=True)
class Forecast:
    """Prévision météo sur plusieurs jours."""

    location: str
    daily: list[DayForecast]
