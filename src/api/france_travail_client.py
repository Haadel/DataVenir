import requests
from src.core.logger import get_logger

logger = get_logger(__name__)


def search_jobs(token, params=None):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    params = params or {}

    logger.info("Calling France Travail API")
    logger.info(f"Params: {params}")

    response = requests.get(url, headers=headers, params=params)

    logger.info(f"HTTP status: {response.status_code}")

    # 🔴 cas erreur
    if response.status_code >= 400:
        logger.error(f"API Error: {response.text}")
        return {
            "status": "error",
            "http_status": response.status_code,
            "data": None,
            "error": response.text
        }

    # 🟡 cas 206 
    if response.status_code == 206:
        logger.warning("Pas d'offres corespondantes à la requête.")
        return {
            "status": "empty",
            "http_status": response.status_code,
            "data": None,
            "error": "Pas d'offres correspondantes à la requête."
        }

    # 🔵 debug réponse brute 
    try:
        data = response.json()
        logger.info(f"Number of results: {len(data.get('resultats', []))}")
    except Exception as e:
        logger.error(f"JSON decode error: {e}")
        return {
            "status": "error",
            "http_status": response.status_code,
            "data": None,
            "error": "Invalid JSON"
        }

    return {
        "status": "success",
        "http_status": response.status_code,
        "data": data,
        "error": None
    }