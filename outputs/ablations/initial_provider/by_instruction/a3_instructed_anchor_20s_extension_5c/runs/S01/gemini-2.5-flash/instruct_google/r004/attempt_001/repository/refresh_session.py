# [SAME-SCENARIO] refresh_session.py - refreshes an expired session or access token
# Provider: Google Firebase Authentication

import requests
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_REFRESH_TOKEN_URL = "https://securetoken.googleapis.com/v1/token?key="

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("Firebase Web API Key not found. Please set FIREBASE_API_KEY environment variable.")

    url = f"{FIREBASE_REFRESH_TOKEN_URL}{FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }

    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status() # Raise an exception for HTTP errors

    data = response.json()
    return RefreshSessionResponse(
        id_token=data["id_token"],
        refresh_token=data["refresh_token"],
        local_id=data["user_id"]
    )
