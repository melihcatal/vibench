# refresh_session.py
import requests
from identity_client import get_firebase_web_api_key
from identity_models import RefreshRequest, RefreshResponse

def refresh_user_session(refresh_request: RefreshRequest) -> RefreshResponse:
    """
    Refreshes an access token using a refresh token via Firebase's Secure Token Service API.
    """
    api_key = get_firebase_web_api_key()
    sts_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token
    }

    response = requests.post(sts_api_url, json=payload)
    response.raise_for_status()

    data = response.json()
    return RefreshResponse(
        id_token=data['id_token'],
        refresh_token=data['refresh_token'],
        expires_in=data['expires_in'],
        token_type=data['token_type'],
        user_id=data['user_id']
    )
