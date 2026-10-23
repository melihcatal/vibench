import os
import requests
from identity_client import FIREBASE_SECURETOKEN_URL, get_api_key
from identity_models import RefreshSessionRequest, RefreshSessionResponse

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    api_key = get_api_key()
    url = f"{FIREBASE_SECURETOKEN_URL}token?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request["refreshToken"]
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {
        "idToken": data["id_token"],
        "refreshToken": data["refresh_token"],
        "expiresIn": data["expires_in"]
    }