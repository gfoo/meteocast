"""Exceptions du domaine meteocast."""

from __future__ import annotations


class MeteocastError(Exception):
    """Erreur de base de meteocast."""


class LocationNotFoundError(MeteocastError):
    """La localité demandée est introuvable (géocodage sans résultat)."""


class ProviderError(MeteocastError):
    """Le fournisseur météo a échoué (réseau, HTTP, ou réponse inattendue)."""
