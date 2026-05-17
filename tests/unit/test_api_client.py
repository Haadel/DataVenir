"""
Tests unitaires pour la récupération des offres d'emploi.

Objectif :
Tester NOTRE fonction search_jobs()
et non l’API réelle France Travail.

On mock requests.get()
pour simuler les réponses de l’API.
"""

from unittest.mock import patch, Mock
import pytest

from src.api.france_travail_client import search_jobs


@patch("src.api.france_travail_client.requests.get")
def test_search_jobs_success(mock_get):
    """
    Cas nominal :
    L'API renvoie une liste d'offres.

    Ce test vérifie que :
    - la fonction retourne bien les données
    - la clé 'resultats' existe
    - le format attendu est correct
    """

    mock_response = Mock()

    # Réponse simulée de l'API
    mock_response.json.return_value = {
        "resultats": [
            {
                "id": "123",
                "intitule": "Data Scientist"
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    # fake_token suffit ici :
    # on ne teste pas l'authentification dans ce fichier
    data = search_jobs("fake_token")

    assert "resultats" in data
    assert isinstance(data["resultats"], list)
    assert len(data["resultats"]) == 1


@patch("src.api.france_travail_client.requests.get")
def test_search_jobs_http_error(mock_get):
    """
    Cas erreur :
    L'API renvoie une erreur HTTP
    (ex: token invalide, quota dépassé, etc.)

    Ce test vérifie que :
    - l'erreur remonte correctement
    - la fonction ne continue pas silencieusement
    """

    mock_response = Mock()

    mock_response.raise_for_status.side_effect = Exception(
        "403 Forbidden"
    )

    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        search_jobs("fake_token")