import requests
from identity_client import get_firebase_api_key
from identity_models import RefreshTokenRequest, RefreshTokenResponse

def refresh_user_token(refresh_request: RefreshTokenRequest) -> RefreshTokenResponse:
    """
    Refreshes an ID token using a refresh token via Firebase Auth REST API.
    """
    api_key = get_firebase_api_key()
    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token
    }

    response = requests.post(rest_api_url, json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()
    return RefreshTokenResponse.model_validate(data)
