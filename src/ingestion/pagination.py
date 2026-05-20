"""
Gestion de la pagination France Travail.

Responsabilité :
- générer les ranges
- récupérer toutes les pages
- arrêter la boucle quand il n'y a plus de résultats
"""

from time import sleep
from src.core.logger import get_logger

logger = get_logger()

#TODO: 

def paginate_search(
    search_function,
    token,
    params,
    page_size=150,
    max_results=3149,
    delay=0.2
):
    """
    Récupère plusieurs pages de résultats.

    Parameters
    ----------
    search_function : callable
        Fonction utilisée pour appeler l'API.
        Exemple : search_jobs()

    token : str
        Token OAuth France Travail.

    params : dict
        Paramètres de recherche.

    page_size : int
        Nombre de résultats par page.

    max_results : int
        Nombre maximum de résultats à récupérer.

    delay : float
        Pause entre les requêtes pour éviter
        de spammer l'API.

    Returns
    -------
    list
        Liste complète des offres récupérées.
    """

    all_jobs = []

    for start in range(0, max_results, page_size):

        end = start + page_size - 1

        # copie locale pour éviter de modifier
        # le dictionnaire original
        current_params = params.copy()

        current_params["range"] = f"{start}-{end}"

        response = search_function(token, current_params)

        if response.get('status') != 'success':
            logger.warning(f"No data returned for range {start}-{end}")
            break

        jobs = response.get("data", []).get("resultats", [])

        all_jobs.extend(jobs)

        logger.debug(f"Fetched {len(jobs)} jobs for range {start}-{end}, total so far: {len(all_jobs)}")
        # évite de spammer l'API
        sleep(delay)

    return all_jobs