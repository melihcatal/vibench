import requests
from identity_models import LoginUserPayload, AuthTokens
from typing import Dict, Any


def email_password_login(payload: LoginUserPayload, config: Dict[str, Any]) -> AuthTokens:
    api_key = config["firebase_web_api_key"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"email": payload.email, "password": payload.password, "returnSecureToken": True}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    response_data = response.json()
    return AuthTokens(
        id_token=response_data["idToken"],
        refresh_token=response_data["refreshToken"],
        expires_in=int(response_data["expiresIn"])
    )
