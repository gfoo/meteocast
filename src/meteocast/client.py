"""API publique *bibliothèque* de meteocast : météo courante et prévisions.

Les fonctions valident leurs entrées puis délèguent au fournisseur choisi via
``source`` (voir ``meteocast.providers`` pour l'abstraction des sources et la
source par défaut Open-Meteo).
"""

from __future__ import annotations

from meteocast.models import DayForecast, Forecast, Weather
from meteocast.providers import (
    DEFAULT_SOURCE,
    get_current_provider,
    get_forecast_provider,
)

DEFAULT_TIMEOUT = 10.0

__all__ = [
    "Weather",
    "DayForecast",
    "Forecast",
    "get_current",
    "get_forecast",
    "DEFAULT_TIMEOUT",
    "DEFAULT_SOURCE",
]


def get_current(
    location: str,
    *,
    source: str = DEFAULT_SOURCE,
    timeout: float = DEFAULT_TIMEOUT,
) -> Weather:
    """Retourne la météo courante pour ``location``.

    Args:
        location: nom de la localité (ville, code postal…).
        source: identifiant du fournisseur météo (défaut : ``"open-meteo"``).
        timeout: délai maximum des requêtes HTTP, en secondes.

    Raises:
        ValueError: si ``location`` est vide ou si ``source`` est inconnu.
        LocationNotFoundError: si la localité est introuvable.
        ProviderError: en cas d'échec réseau/HTTP ou de réponse inattendue.
    """
    if not location.strip():
        raise ValueError("location ne doit pas être vide")
    provider = get_current_provider(source)
    return provider.get_current(location, timeout=timeout)


def get_forecast(
    location: str,
    *,
    days: int = 3,
    source: str = DEFAULT_SOURCE,
    timeout: float = DEFAULT_TIMEOUT,
) -> Forecast:
    """Retourne la prévision sur ``days`` jours pour ``location``.

    Args:
        location: nom de la localité (ville, code postal…).
        days: nombre de jours de prévision (1 à 16).
        source: identifiant du fournisseur météo (défaut : ``"open-meteo"``).
        timeout: délai maximum des requêtes HTTP, en secondes.

    Raises:
        ValueError: si ``location`` est vide, ``days`` hors bornes, ou ``source`` inconnu.
        LocationNotFoundError: si la localité est introuvable.
        ProviderError: en cas d'échec réseau/HTTP ou de réponse inattendue.
    """
    if not location.strip():
        raise ValueError("location ne doit pas être vide")
    if not 1 <= days <= 16:
        raise ValueError("days doit être compris entre 1 et 16")
    provider = get_forecast_provider(source)
    return provider.get_forecast(location, days=days, timeout=timeout)
