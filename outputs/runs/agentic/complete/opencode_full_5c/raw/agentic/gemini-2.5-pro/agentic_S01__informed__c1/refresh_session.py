import requests
from identity_client import get_firebase_web_api_key
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_request: RefreshRequest) -> RefreshResponse:
    """
    Refreshes an access token using a refresh token via Firebase Auth REST API.
    """
    api_key = get_firebase_web_api_key()
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    return RefreshResponse(
        id_token=data["id_token"],
        refresh_token=data["refresh_token"],
        expires_in=int(data["expires_in"]),
        user_id=data["user_id"],
    )
