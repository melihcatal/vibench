import requests
from identity_client import get_firebase_api_key
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_AUTH_REFRESH_URL = "https://securetoken.googleapis.com/v1/token?key="

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    api_key = get_firebase_api_key()
    url = f"{FIREBASE_AUTH_REFRESH_URL}{api_key}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return RefreshSessionResponse(
        id_token=data["id_token"],
        refresh_token=data["refresh_token"],
        expires_in=int(data["expires_in"])
    )
