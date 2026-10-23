import os
from identity_client import initiate_password_reset, AUTH0_CONNECTION
from identity_models import PasswordResetRequest, PasswordResetResponse


def start_password_reset(email: str, connection: str = None) -> PasswordResetResponse:
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "")

    if not auth0_domain:
        raise ValueError(
            "AUTH0_DOMAIN environment variable is required for Auth0 password reset"
        )

    req = PasswordResetRequest(
        email=email,
        connection=connection or AUTH0_CONNECTION,
    )

    result = initiate_password_reset(req=req)
    return result
