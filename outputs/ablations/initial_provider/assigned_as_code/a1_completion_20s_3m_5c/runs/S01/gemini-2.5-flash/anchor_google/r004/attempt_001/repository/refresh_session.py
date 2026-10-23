import requests
from identity_models import RefreshSessionPayload, AuthTokens
from typing import Dict, Any


def refresh_session(payload: RefreshSessionPayload, config: Dict[str, Any]) -> AuthTokens:
    api_key = config["firebase_web_api_key"]
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"grant_type": "refresh_token", "refresh_token": payload.refresh_token}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    response_data = response.json()
    return AuthTokens(
        id_token=response_data["id_token"],
        refresh_token=response_data["refresh_token"],
        expires_in=int(response_data["expires_in"])
    )
