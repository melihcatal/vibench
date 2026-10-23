from __future__ import annotations

from typing import Dict

from identity_client import get_auth0_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> Dict[str, str]:
    client = get_auth0_client()
    request = PasswordResetRequest(email=email)
    client.password_change(email=request.email, connection=request.connection)
    return PasswordResetResponse(
        email=email, status="password_reset_requested"
    ).to_dict()
