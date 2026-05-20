
"""
Orchestration de la récupération des offres.
"""

from src.auth.france_travail_auth import get_access_token
from src.api.france_travail_client import search_jobs
from src.ingestion.raw_saver import save_raw_jobs
from src.ingestion.pagination import paginate_search
from src.ingestion.search_queries import SEARCH_QUERIES
from src.core.logger import get_logger
import time


BASE_PARAMS = {
    "grandDomaine": "M18",
    "typeContrat": "CDI,CDD",
    "publieeDepuis": 14, # max api = 14 jours
    "sort": 1,
}


def fetch_jobs():
    """
    Récupère les offres pour toutes
    les catégories définies.
    """


    logger = get_logger(__name__)

    start_total = time.perf_counter()

    logger.info(f"Starting fetch_jobs, queries={len(SEARCH_QUERIES)}")

    try:
        token = get_access_token()
    except Exception:
        logger.exception("Failed to obtain access token")
        raise

    all_jobs = []

    for category, query_params in SEARCH_QUERIES.items():

        params = BASE_PARAMS | query_params

        logger.info(f"Start category={category}, params={{{', '.join(params.keys())}}}")
        cat_start = time.perf_counter()

        try:
            jobs = paginate_search(
                search_function=search_jobs,
                token=token,
                params=params,
                page_size=150,
            )

            filename = f"{category}.json"
            save_raw_jobs(
                jobs,
                filename=filename
            )

            all_jobs.extend(jobs)

            cat_elapsed = int((time.perf_counter() - cat_start) * 1000)
            logger.info(
                f"End category={category}, fetched={len(jobs)}, saved={filename}, elapsed_ms={cat_elapsed}"
            )

        except Exception:
            logger.exception("Error fetching category", extra={"category": category})
            # continue with next category
            continue

    # suppression doublons via id
    before_count = len(all_jobs)
    unique_jobs = {
        job["id"]: job
        for job in all_jobs
    }

    result = list(unique_jobs.values())

    total_elapsed = int((time.perf_counter() - start_total) * 1000)
    logger.info(
        f"Finished fetch_jobs, before_dedup={before_count}, unique_jobs={len(result)}, total_elapsed_ms={total_elapsed}"
    )

    return result





if __name__ == "__main__":
    jobs = fetch_jobs()
    print(jobs)