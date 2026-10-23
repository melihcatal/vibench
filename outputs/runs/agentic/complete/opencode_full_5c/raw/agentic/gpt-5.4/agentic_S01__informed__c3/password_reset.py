import requests

from identity_client import (
    auth0_client_id,
    auth0_connection,
    auth0_domain,
    request_timeout,
)
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest):
    payload = {
        "client_id": auth0_client_id(),
        "email": request.email,
        "connection": request.connection or auth0_connection(),
    }
    response = requests.post(
        f"https://{auth0_domain()}/dbconnections/change_password",
        json=payload,
        timeout=request_timeout(),
    )
    response.raise_for_status()
    return {
        "email": request.email,
        "connection": payload["connection"],
        "message": response.text,
    }
