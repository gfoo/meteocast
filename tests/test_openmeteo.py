"""Tests du fournisseur Open-Meteo, avec le réseau simulé (httpx.MockTransport)."""

import httpx
import pytest

from meteocast.errors import LocationNotFoundError, ProviderError
from meteocast.models import DayForecast, Forecast, Weather
from meteocast.providers.openmeteo import OpenMeteoProvider

GEO_OK = {
    "results": [{"name": "Lausanne", "country": "Suisse", "latitude": 46.516, "longitude": 6.632}]
}


def _provider(handler) -> OpenMeteoProvider:
    return OpenMeteoProvider(transport=httpx.MockTransport(handler))


def _is_geocoding(request: httpx.Request) -> bool:
    return "geocoding" in request.url.host


def test_get_current_maps_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if _is_geocoding(request):
            return httpx.Response(200, json=GEO_OK)
        return httpx.Response(200, json={"current": {"temperature_2m": 21.3, "weather_code": 3}})

    weather = _provider(handler).get_current("Lausanne", timeout=5)
    assert isinstance(weather, Weather)
    assert weather.location == "Lausanne, Suisse"
    assert weather.temperature_c == 21.3
    assert weather.description == "Couvert"


def test_get_forecast_maps_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if _is_geocoding(request):
            return httpx.Response(200, json=GEO_OK)
        return httpx.Response(
            200,
            json={
                "daily": {
                    "time": ["2026-07-05", "2026-07-06"],
                    "temperature_2m_max": [26.0, 24.5],
                    "temperature_2m_min": [14.0, 13.5],
                    "weather_code": [0, 61],
                }
            },
        )

    forecast = _provider(handler).get_forecast("Lausanne", days=2, timeout=5)
    assert isinstance(forecast, Forecast)
    assert forecast.location == "Lausanne, Suisse"
    assert len(forecast.daily) == 2
    first = forecast.daily[0]
    assert isinstance(first, DayForecast)
    assert first.date == "2026-07-05"
    assert first.temperature_min_c == 14.0
    assert first.temperature_max_c == 26.0
    assert first.description == "Ciel dégagé"
    assert forecast.daily[1].description == "Pluie faible"


def test_location_not_found() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"results": []})

    with pytest.raises(LocationNotFoundError):
        _provider(handler).get_current("Xyzzy", timeout=5)


def test_http_error_becomes_provider_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    with pytest.raises(ProviderError):
        _provider(handler).get_current("Lausanne", timeout=5)


def test_unexpected_payload_becomes_provider_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if _is_geocoding(request):
            return httpx.Response(200, json=GEO_OK)
        return httpx.Response(200, json={"current": {}})  # champs manquants

    with pytest.raises(ProviderError):
        _provider(handler).get_current("Lausanne", timeout=5)
