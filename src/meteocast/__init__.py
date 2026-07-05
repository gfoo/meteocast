"""meteocast — bibliothèque et CLI pour les informations météo et prévisions."""

from meteocast.client import Forecast, Weather, get_current, get_forecast

__version__ = "0.1.0"

__all__ = ["Forecast", "Weather", "get_current", "get_forecast", "__version__"]
