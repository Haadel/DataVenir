"""
Sauvegarde et chargement des données RAW.
"""

import json
from pathlib import Path
from datetime import datetime
from src.core.logger import get_logger


logger = get_logger(__name__)
#TODO: ajouter des logs pour le nombre d'offres sauvegardées, les erreurs de lecture/écriture, etc.

def find_project_root(path: Path = None) -> Path:
    """
    Recherche la racine du projet en remontant les dossiers à partir de `path`.
    On considère comme racine un dossier contenant l'un des fichiers/marqueurs :
    .git, pyproject.toml, setup.cfg, requirements.txt, README.md
    Si rien n'est trouvé, on retourne le dossier courant de travail.
    """

    if path is None:
        path = Path(__file__).resolve()

    for parent in [path] + list(path.parents):
        for marker in (".git", "pyproject.toml", "setup.cfg", "requirements.txt", "README.md"):
            if (Path(parent) / marker).exists():
                return Path(parent)

    return Path.cwd()


# Toujours utiliser le dossier data/raw à la racine du projet
RAW_DATA_DIR = find_project_root() / "data" / "raw"

def get_today_directory():
    """
    Retourne le dossier du jour.

    Exemple :
    data/raw/2026-05-20/
    """

    today = datetime.now().strftime("%Y-%m-%d")

    directory = RAW_DATA_DIR / today

    directory.mkdir(parents=True, exist_ok=True)

    return directory


def save_raw_jobs(jobs, filename): 
    """
    Sauvegarde une liste d'offres
    au format JSON.

    Parameters
    ----------
    jobs : list
        Liste des offres.

    filename : str
        Nom du fichier.
        Exemple : data_scientist.json
    """

    directory = get_today_directory()

    filepath = directory / filename

    with open(filepath, "w", encoding="utf-8") as f:

        json.dump(
            jobs,
            f,
            ensure_ascii=False,
            indent=2
        )
    logger.info(f"Saved {len(jobs)} jobs to {filepath}")


def load_raw_jobs(filepath):
    """
    Charge un fichier RAW JSON.
    """

    with open(filepath, "r", encoding="utf-8") as f:

        return json.load(f)