from __future__ import annotations

from identity_client import Auth0Client
from identity_models import EmailPasswordRequest, TokenResponse


def email_password_login(email: str, password: str) -> TokenResponse:
    client = Auth0Client()
    req = EmailPasswordRequest(email=email, password=password)
    data = client.token(
        {
            "grant_type": "password",
            "username": req.normalized_email(),
            "password": req.password,
            "client_id": client.config.auth0_client_id,
            "audience": client.config.auth0_audience,
            "scope": "openid profile email offline_access",
        }
    )
    return TokenResponse.from_dict(data)
