from __future__ import annotations

from identity_client import Auth0Client, load_auth0_config
from identity_models import LoginRequest, TokenResponse


def email_password_login(email: str, password: str, audience: str | None = None) -> dict:
    config = load_auth0_config()
    client = Auth0Client(config)
    request = LoginRequest(email=email, password=password, audience=audience or config.audience)
    response = client.post(
        "/oauth/token",
        request.to_auth0_payload(client_id=config.client_id, client_secret=config.client_secret),
    )
    return TokenResponse.from_auth0(response).to_dict()
