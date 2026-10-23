import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
if not FIREBASE_WEB_API_KEY:
    raise EnvironmentError("FIREBASE_WEB_API_KEY environment variable not set.")

FIREBASE_REFRESH_TOKEN_URL = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"

def refresh_user_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }
    response = requests.post(FIREBASE_REFRESH_TOKEN_URL, json=payload)
    response.raise_for_status()
    data = response.json()

    return RefreshSessionResponse(
        id_token=data["id_token"],
        refresh_token=data["refresh_token"] if "refresh_token" in data else request.refresh_token,
        expires_in=int(data["expires_in"]),
        user_id=data["user_id"]
    )