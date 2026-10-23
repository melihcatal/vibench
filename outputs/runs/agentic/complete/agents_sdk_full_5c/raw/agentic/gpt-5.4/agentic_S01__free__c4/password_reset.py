from __future__ import annotations

from identity_client import identity_toolkit_url, post_json
from identity_models import PasswordResetRequest



def password_reset(email: str) -> dict:
    request_model = PasswordResetRequest(email=email)
    return post_json(identity_toolkit_url("sendOobCode"), request_model.to_identity_toolkit_payload())
