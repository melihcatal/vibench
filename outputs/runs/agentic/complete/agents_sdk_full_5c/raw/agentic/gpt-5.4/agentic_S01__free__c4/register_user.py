from __future__ import annotations

from identity_client import identity_toolkit_url, post_json
from identity_models import RegisterUserRequest, UserAccount, parse_auth_response



def register_user(email: str, password: str, display_name: str | None = None) -> UserAccount:
    request_model = RegisterUserRequest(email=email, password=password, display_name=display_name)
    response_data = post_json(identity_toolkit_url("signUp"), request_model.to_identity_toolkit_payload())
    return parse_auth_response(response_data)
