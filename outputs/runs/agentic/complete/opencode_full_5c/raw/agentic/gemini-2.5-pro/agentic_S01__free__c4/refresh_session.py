import os
import requests
from identity_models import RefreshRequest, AuthResponse


def refresh_user_session(refresh_request: RefreshRequest) -> AuthResponse:
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()

    return AuthResponse(
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        expires_in=int(data.get("expires_in")),
        local_id=data.get("user_id"),
    )
