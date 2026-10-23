import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    firebase_api_key = os.environ.get("FIREBASE_API_KEY")
    if not firebase_api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={firebase_api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token
    }

    response = requests.post(rest_api_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return RefreshSessionResponse(
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        expires_in=data.get("expires_in")
    )
