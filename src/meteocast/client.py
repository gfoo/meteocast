"""Client bas niveau pour récupérer météo courante et prévisions.

Ce module expose l'API *bibliothèque* de meteocast. L'intégration d'une API
météo réelle (par ex. Open-Meteo) n'est pas encore branchée : les fonctions
valident leurs entrées et lèvent ``NotImplementedError`` en attendant.
"""

from __future__ import annotations

from dataclasses import dataclass

import httpx

DEFAULT_TIMEOUT = 10.0


@dataclass(slots=True)
class Weather:
    """Conditions météo à un instant donné."""

    location: str
    temperature_c: float
    description: str


@dataclass(slots=True)
class Forecast:
    """Prévision météo sur plusieurs jours."""

    location: str
    daily: list[Weather]


def get_current(location: str, *, timeout: float = DEFAULT_TIMEOUT) -> Weather:
    """Retourne la météo courante pour ``location``.

    Args:
        location: nom de la localité (ville, code postal…).
        timeout: délai maximum des requêtes HTTP, en secondes.

    Raises:
        ValueError: si ``location`` est vide.
        NotImplementedError: tant qu'aucune API météo n'est branchée.
    """
    if not location.strip():
        raise ValueError("location ne doit pas être vide")

    with httpx.Client(timeout=timeout) as _client:
        raise NotImplementedError("L'intégration d'une API météo n'est pas encore implémentée.")


def get_forecast(location: str, *, days: int = 3, timeout: float = DEFAULT_TIMEOUT) -> Forecast:
    """Retourne la prévision sur ``days`` jours pour ``location``.

    Args:
        location: nom de la localité (ville, code postal…).
        days: nombre de jours de prévision (1 à 16).
        timeout: délai maximum des requêtes HTTP, en secondes.

    Raises:
        ValueError: si ``location`` est vide ou si ``days`` est hors bornes.
        NotImplementedError: tant qu'aucune API météo n'est branchée.
    """
    if not location.strip():
        raise ValueError("location ne doit pas être vide")
    if not 1 <= days <= 16:
        raise ValueError("days doit être compris entre 1 et 16")

    with httpx.Client(timeout=timeout) as _client:
        raise NotImplementedError("L'intégration d'une API météo n'est pas encore implémentée.")
