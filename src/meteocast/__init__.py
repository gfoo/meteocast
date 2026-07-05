"""meteocast — bibliothèque et CLI pour les informations météo et prévisions."""

from meteocast.client import (
    DEFAULT_SOURCE,
    DEFAULT_TIMEOUT,
    DayForecast,
    Forecast,
    Weather,
    get_current,
    get_forecast,
)
from meteocast.errors import LocationNotFoundError, MeteocastError, ProviderError

__version__ = "0.2.0"

__all__ = [
    "Weather",
    "DayForecast",
    "Forecast",
    "get_current",
    "get_forecast",
    "MeteocastError",
    "LocationNotFoundError",
    "ProviderError",
    "DEFAULT_SOURCE",
    "DEFAULT_TIMEOUT",
    "__version__",
]
