"""Fournisseur Open-Meteo (gratuit, sans clé API).

Deux étapes pour chaque requête : géocodage de la localité (nom → coordonnées)
via l'API de géocodage, puis récupération de la météo via l'API de prévision.
Implémente les deux abstractions : météo courante *et* prévision.
"""

from __future__ import annotations

import httpx

from meteocast.errors import LocationNotFoundError, ProviderError
from meteocast.models import DayForecast, Forecast, Weather
from meteocast.wmo import describe


class OpenMeteoProvider:
    """Météo courante et prévisions via l'API Open-Meteo."""

    name = "open-meteo"

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, *, transport: httpx.BaseTransport | None = None) -> None:
        # ``transport`` permet d'injecter un httpx.MockTransport dans les tests ;
        # en production il reste None (transport HTTP réel par défaut).
        self._transport = transport

    def _client(self, timeout: float) -> httpx.Client:
        return httpx.Client(timeout=timeout, transport=self._transport)

    def _geocode(self, client: httpx.Client, location: str) -> tuple[float, float, str]:
        """Résout ``location`` en (latitude, longitude, libellé lisible)."""
        try:
            resp = client.get(
                self.GEOCODING_URL,
                params={"name": location, "count": 1, "language": "fr", "format": "json"},
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as exc:
            raise ProviderError(f"Échec du géocodage de {location!r} : {exc}") from exc

        results = data.get("results") or []
        if not results:
            raise LocationNotFoundError(f"Localité introuvable : {location!r}")

        top = results[0]
        try:
            name = top["name"]
            country = top.get("country")
            label = f"{name}, {country}" if country else name
            return float(top["latitude"]), float(top["longitude"]), label
        except (KeyError, TypeError, ValueError) as exc:
            raise ProviderError(f"Réponse de géocodage inattendue : {exc}") from exc

    def _fetch(self, client: httpx.Client, params: dict[str, object]) -> dict:
        try:
            resp = client.get(self.FORECAST_URL, params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as exc:
            raise ProviderError(f"Échec de récupération météo : {exc}") from exc

    def get_current(self, location: str, *, timeout: float) -> Weather:
        with self._client(timeout) as client:
            lat, lon, label = self._geocode(client, location)
            data = self._fetch(
                client,
                {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,weather_code",
                    "timezone": "auto",
                },
            )
        try:
            current = data["current"]
            return Weather(
                location=label,
                temperature_c=float(current["temperature_2m"]),
                description=describe(int(current["weather_code"])),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ProviderError(f"Réponse météo inattendue : {exc}") from exc

    def get_forecast(self, location: str, *, days: int, timeout: float) -> Forecast:
        with self._client(timeout) as client:
            lat, lon, label = self._geocode(client, location)
            data = self._fetch(
                client,
                {
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                    "forecast_days": days,
                    "timezone": "auto",
                },
            )
        try:
            daily = data["daily"]
            entries = [
                DayForecast(
                    date=date,
                    temperature_min_c=float(tmin),
                    temperature_max_c=float(tmax),
                    description=describe(int(code)),
                )
                for date, tmin, tmax, code in zip(
                    daily["time"],
                    daily["temperature_2m_min"],
                    daily["temperature_2m_max"],
                    daily["weather_code"],
                    strict=True,
                )
            ]
        except (KeyError, TypeError, ValueError) as exc:
            raise ProviderError(f"Réponse de prévision inattendue : {exc}") from exc
        return Forecast(location=label, daily=entries)
