from __future__ import annotations

from identity_client import identity_toolkit_url, post_json
from identity_models import LoginRequest, UserAccount, parse_auth_response



def email_password_login(email: str, password: str) -> UserAccount:
    request_model = LoginRequest(email=email, password=password)
    response_data = post_json(identity_toolkit_url("signInWithPassword"), request_model.to_identity_toolkit_payload())
    return parse_auth_response(response_data)
