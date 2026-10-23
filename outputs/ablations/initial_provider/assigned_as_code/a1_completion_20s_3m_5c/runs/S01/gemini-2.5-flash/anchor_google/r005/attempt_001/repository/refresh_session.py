import requests
import os
from identity_models import RefreshSessionPayload

def refresh_session(payload: RefreshSessionPayload):
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": payload.refresh_token
    }

    response = requests.post(rest_api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
