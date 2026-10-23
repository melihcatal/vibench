import requests

from identity_client import (
    auth0_auth_base_url,
    auth0_audience,
    auth0_client_id,
    auth0_client_secret,
)
from identity_models import normalize_email, response_payload


def email_password_login(email: str, password: str):
    payload = {
        "grant_type": "password",
        "username": normalize_email(email),
        "password": password,
        "client_id": auth0_client_id(),
        "scope": "openid profile email",
    }
    secret = auth0_client_secret()
    audience = auth0_audience()
    if secret:
        payload["client_secret"] = secret
    if audience:
        payload["audience"] = audience
    r = requests.post(f"{auth0_auth_base_url()}/oauth/token", json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return response_payload(
        {
            "provider": "Auth0",
            "access_token": data.get("access_token"),
            "id_token": data.get("id_token"),
            "refresh_token": data.get("refresh_token"),
            "token_type": data.get("token_type"),
            "expires_in": data.get("expires_in"),
        }
    )
