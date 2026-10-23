import requests

from identity_models import normalize_email


def password_reset(payload, config=None):
    config = config or {}
    api_key = config.get("firebase_web_api_key")
    email = normalize_email(payload["email"])
    response = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode",
        params={"key": api_key},
        json={"requestType": "PASSWORD_RESET", "email": email},
        timeout=30,
    )
    response.raise_for_status()
    return {"email": email, "reset_email_sent": True, "provider_response": response.json()}
