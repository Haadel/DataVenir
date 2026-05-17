
"""
Tests unitaires pour la récupération du token OAuth France Travail.

Objectif :
Tester NOTRE fonction get_access_token()
et non pas l’API réelle de France Travail.

On mock donc requests.post() pour simuler
les réponses du serveur sans faire d'appel réseau.
"""

from unittest.mock import patch, Mock
import pytest

from src.auth.france_travail_auth import get_access_token


@patch("src.auth.france_travail_auth.requests.post")
def test_get_access_token_success(mock_post):
    """
    Cas nominal :
    L'API renvoie correctement un token.

    Ce test vérifie que :
    - la fonction retourne bien le token
    - aucune exception n'est levée
    """

    # On crée une fausse réponse HTTP
    mock_response = Mock()

    # On simule le JSON retourné par l'API
    mock_response.json.return_value = {
        "access_token": "fake_token_123"
    }

    # raise_for_status() ne fait rien ici
    # car la réponse est supposée être un succès (HTTP 200)
    mock_response.raise_for_status.return_value = None

    # requests.post() retournera cette fausse réponse
    mock_post.return_value = mock_response

    # On appelle NOTRE fonction
    token = get_access_token()

    # Vérification du résultat attendu
    assert token == "fake_token_123"


@patch("src.auth.france_travail_auth.requests.post")
def test_get_access_token_http_error(mock_post):
    """
    Cas erreur :
    L'API renvoie une erreur HTTP
    (ex: 401 Unauthorized).

    Ce test vérifie que :
    - la fonction ne masque pas l'erreur
    - une exception est bien levée
    """

    mock_response = Mock()

    # On force raise_for_status() à lever une exception
    mock_response.raise_for_status.side_effect = Exception(
        "401 Unauthorized"
    )

    mock_post.return_value = mock_response

    # pytest vérifie qu'une exception est bien levée
    with pytest.raises(Exception):
        get_access_token()