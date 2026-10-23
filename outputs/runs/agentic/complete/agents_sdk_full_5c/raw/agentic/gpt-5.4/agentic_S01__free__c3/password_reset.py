from __future__ import annotations

from identity_client import Auth0Client, load_auth0_settings
from identity_models import PasswordResetRequest


def password_reset(email: str) -> dict:
    settings = load_auth0_settings()
    client = Auth0Client(settings=settings)
    request = PasswordResetRequest(email=email)
    result = client.start_password_reset(request.to_reset_payload(settings.client_id))
    return {"provider": "auth0", "result": result}
