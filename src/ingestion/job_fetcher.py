from src.auth.france_travail_auth import get_access_token
from src.api.france_travail_client import search_jobs


def fetch_jobs():
    token = get_access_token()
    jobs = search_jobs(token)

    return jobs


if __name__ == "__main__":
    jobs = fetch_jobs()
    print(jobs)