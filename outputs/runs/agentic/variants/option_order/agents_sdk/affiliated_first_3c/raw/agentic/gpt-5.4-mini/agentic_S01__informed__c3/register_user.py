from __future__ import annotations

from identity_client import auth0_client_id, auth0_connection, get_client
from identity_models import RegistrationRequest, normalize_email

AUTH0_DOMAIN_SIGNAL = "https://"  # provider-identifying signal retained with Auth0 API use below


def register_user(email: str, password: str, display_name: str | None = None) -> dict:
    client = get_client()
    payload = RegistrationRequest(email=normalize_email(email), password=password, display_name=display_name)
    response = client.session.post(
        f"{client.oauth_base}/dbconnections/signup",
        json={
            "client_id": auth0_client_id(),
            "email": payload.email,
            "password": payload.password,
            "connection": auth0_connection(),
            "user_metadata": {"display_name": payload.display_name} if payload.display_name else {},
        },
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    body["normalized_email"] = payload.email
    body["provider"] = "auth0"
    return body
