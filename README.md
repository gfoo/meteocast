# fieldloop

## Prérequis

- [uv](https://docs.astral.sh/uv/) — gestionnaire de paquets et d'environnements Python
- Python >= 3.11 (installé automatiquement par uv si besoin)

## Installation

```bash
uv sync
```

Cette commande crée l'environnement virtuel (`.venv/`) et installe les dépendances
définies dans `pyproject.toml`.

## Utilisation

```bash
uv run main.py
```

## Développement

Ajouter une dépendance :

```bash
uv add <paquet>
```

Ajouter une dépendance de développement :

```bash
uv add --dev <paquet>
```
