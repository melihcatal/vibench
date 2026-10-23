from __future__ import annotations

from identity_client import firebase_post
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest):
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email,
    }
    return firebase_post("accounts:sendOobCode", payload)
