import requests

from identity_client import auth0_auth_base_url, auth0_client_id, auth0_client_secret
from identity_models import EmailPasswordUserInput, response_payload


def register_user(
    email: str, password: str, locale: str = "en", display_name: str = None
):
    user = EmailPasswordUserInput(
        email=email, password=password, locale=locale, display_name=display_name
    ).normalized()
    payload = {
        "client_id": auth0_client_id(),
        "email": user["email"],
        "password": user["password"],
        "connection": "Username-Password-Authentication",
        "user_metadata": {
            "locale": user["locale"],
            "display_name": user["display_name"],
        },
    }
    secret = auth0_client_secret()
    if secret:
        payload["client_secret"] = secret
    r = requests.post(
        f"{auth0_auth_base_url()}/dbconnections/signup", json=payload, timeout=30
    )
    r.raise_for_status()
    data = r.json()
    return response_payload(
        {
            "provider": "Auth0",
            "user_id": data.get("_id") or data.get("user_id"),
            "email": user["email"],
            "status": data.get("status") or "created",
        }
    )
