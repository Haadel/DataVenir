import requests


def search_jobs(token):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "grandDomaine": "M18",
        "typeContrat": "CDI,CDD",
        "publieeDepuis": 7,
        "sort": 1,
        "range": "0-49",
        "motsCles": "data,python,sql"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()