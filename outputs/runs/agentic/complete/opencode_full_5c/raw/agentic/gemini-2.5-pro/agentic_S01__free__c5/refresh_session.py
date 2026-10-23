import requests
from identity_client import get_firebase_api_key, get_secure_token_url
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_id_token(refresh_request: RefreshSessionRequest) -> RefreshSessionResponse:
    api_key = get_firebase_api_key()
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    url = f"{get_secure_token_url()}?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    return RefreshSessionResponse(**data)
