# meteocast

**meteocast** est une bibliothèque *et* une CLI Python pour récupérer des
informations météo et des données de prévision.

- 🖥️ **CLI** : consultez la météo depuis votre terminal.
- 🐍 **Bibliothèque** : intégrez la récupération de données dans votre code Python.

> ℹ️ **État du projet** : la récupération réelle est branchée sur
> [Open-Meteo](https://open-meteo.com) (gratuit, sans clé API). L'accès aux
> sources passe par une abstraction (`meteocast.providers`) prévue pour brancher
> d'autres fournisseurs — de météo courante et/ou de prévision — via l'option
> `--source` (CLI) ou l'argument `source=` (bibliothèque).

---

## Utiliser la CLI

### Depuis PyPI

Le plus simple, sans rien installer de permanent, avec [uv](https://docs.astral.sh/uv/) :

```bash
uvx meteocast forecast Lausanne
```

`uvx` télécharge meteocast dans un environnement éphémère et l'exécute.

Pour l'installer durablement comme outil isolé :

```bash
uv tool install meteocast     # via uv
# ou
pipx install meteocast        # via pipx
```

La commande `meteocast` est alors disponible partout :

```bash
$ meteocast --help
Usage: meteocast [OPTIONS] COMMAND [ARGS]...

  Récupère des informations météo et des prévisions.

Commands:
  current   Affiche la météo courante pour une localité.
  forecast  Affiche la prévision sur plusieurs jours pour une localité.

$ meteocast forecast Lausanne --days 5
Prévision sur 5 jours pour Lausanne, Suisse
  2026-07-05 : 14.0 – 26.0 °C — Ciel dégagé
  ...

# Choisir explicitement la source (par défaut : open-meteo)
$ meteocast current Lausanne --source open-meteo
```

### Depuis un registre privé JFrog Artifactory

Si meteocast est publié sur votre Artifactory interne, pointez l'installeur
vers l'index privé et fournissez vos identifiants :

```bash
# uv
uv tool install \
  --index "https://<host>/artifactory/api/pypi/<repo>/simple/" \
  meteocast

# pipx
pipx install \
  --index-url "https://<user>:<token>@<host>/artifactory/api/pypi/<repo>/simple/" \
  meteocast
```

---

## Utiliser la bibliothèque

### Depuis PyPI

Ajoutez meteocast à votre projet :

```bash
uv add meteocast
# ou
pip install meteocast
```

Puis, dans votre code :

```python
from meteocast import get_current, get_forecast

# Météo courante
weather = get_current("Lausanne")
print(weather.location, weather.temperature_c, weather.description)

# Prévision sur 5 jours (min / max par jour)
forecast = get_forecast("Lausanne", days=5)
for day in forecast.daily:
    print(day.date, day.temperature_min_c, day.temperature_max_c, day.description)

# Choisir une source explicitement
forecast = get_forecast("Lausanne", days=5, source="open-meteo")
```

### Depuis un registre privé JFrog Artifactory

Décommentez et renseignez le bloc `[[tool.uv.index]]` dans `pyproject.toml` :

```toml
[[tool.uv.index]]
name = "artifactory"
url = "https://<host>/artifactory/api/pypi/<repo>/simple/"
```

Exportez les identifiants, puis synchronisez :

```bash
export UV_INDEX_ARTIFACTORY_USERNAME="<user>"
export UV_INDEX_ARTIFACTORY_PASSWORD="<token>"
uv add meteocast
```

Avec pip, sans uv :

```bash
pip install \
  --extra-index-url "https://<user>:<token>@<host>/artifactory/api/pypi/<repo>/simple/" \
  meteocast
```

L'import Python est ensuite identique à l'exemple ci-dessus.

---

## Développement

Prérequis : [uv](https://docs.astral.sh/uv/) (Python ≥ 3.11 est installé
automatiquement au besoin).

```bash
uv sync                       # crée .venv/ et installe deps + outils de dev
uv run meteocast --help       # lance la CLI en local
uv run ruff check .           # lint
uv run ruff format .          # formatage
uv run pytest                 # tests
```

---

## Publier une version

### Sur PyPI (automatisé)

La publication est automatique via GitHub Actions
(`.github/workflows/release.yml`) en **Trusted Publishing** (OIDC, sans token) :

1. Enregistrer le *publisher* du dépôt sur https://pypi.org/manage/account/publishing/
   (nom du projet `meteocast`, workflow `release.yml`).
2. Mettre à jour `__version__` dans `src/meteocast/__init__.py`.
3. Taguer et pousser :
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
   Le workflow lint, teste, build (`uv build`) et publie (`uv publish`).

Publication manuelle si besoin :

```bash
uv build          # génère dist/*.whl et dist/*.tar.gz
uv publish        # nécessite un token PyPI (UV_PUBLISH_TOKEN)
```

### Sur un registre privé JFrog Artifactory

```bash
uv build
uv publish \
  --publish-url "https://<host>/artifactory/api/pypi/<repo>/" \
  --token "$UV_PUBLISH_TOKEN"
```

(ou `--username <user> --password <token>`). Une étape équivalente commentée est
prête dans `release.yml` pour automatiser cette publication.
