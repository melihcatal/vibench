from __future__ import annotations

from identity_client import Auth0Client, load_auth0_settings
from identity_models import LoginRequest, TokenResponse


def email_password_login(email: str, password: str) -> dict:
    settings = load_auth0_settings()
    client = Auth0Client(settings=settings)
    request = LoginRequest(email=email, password=password, audience=settings.audience)
    payload = client.password_grant_login(request.to_token_payload(settings.client_id, settings.client_secret))
    return TokenResponse.from_auth0(payload).to_dict()
