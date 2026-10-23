import requests

from identity_models import normalize_email


def refresh_session(payload, config=None):
    config = config or {}
    api_key = config.get("firebase_web_api_key")
    refresh_token = payload["refresh_token"]
    response = requests.post(
        "https://securetoken.googleapis.com/v1/token",
        params={"key": api_key},
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "email": normalize_email(payload.get("email")),
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in"),
        "user_id": data.get("user_id"),
    }
