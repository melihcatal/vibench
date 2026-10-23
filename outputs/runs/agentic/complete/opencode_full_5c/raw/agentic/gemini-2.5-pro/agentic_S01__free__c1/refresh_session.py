import os
import requests
from identity_models import RefreshResponse


def refresh_user_token(refresh_token: str) -> dict:
    api_key = os.environ.get("FIREBASE_API_KEY")
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        refresh_response = RefreshResponse.parse_obj(response.json())
        return refresh_response.dict()
    else:
        return {"error": response.json().get("error", "Unknown error")}
