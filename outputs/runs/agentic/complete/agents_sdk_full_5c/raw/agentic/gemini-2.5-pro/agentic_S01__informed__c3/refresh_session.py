import requests
from identity_client import get_firebase_api_key
from identity_models import RefreshResponse

# Firebase Authentication REST API endpoint for refreshing a token
FIREBASE_REFRESH_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"

def refresh_user_token(refresh_token: str) -> RefreshResponse:
    """
    Refreshes an ID token using a refresh token via Firebase REST API.

    Args:
        refresh_token: The user's refresh token.

    Returns:
        A RefreshResponse object with new tokens.
    """
    api_key = get_firebase_api_key()
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    params = {"key": api_key}

    response = requests.post(FIREBASE_REFRESH_TOKEN_URL, params=params, json=payload)
    response.raise_for_status()

    data = response.json()
    return RefreshResponse(
        id_token=data['id_token'],
        refresh_token=data['refresh_token'],
        expires_in=data['expires_in'],
        token_type=data['token_type'],
        user_id=data['user_id']
    )
