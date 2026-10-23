import os
import httpx
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_password_reset_response,
)


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")


def password_reset(email, connection="Username-Password-Authentication"):
    req = PasswordResetRequest(
        email=email, connection=connection, client_id=AUTH0_CLIENT_ID
    )
    url = "https://{}/dbconnections/change_password".format(AUTH0_DOMAIN)
    body = {
        "client_id": req.client_id,
        "email": req.email,
        "connection": req.connection,
    }
    resp = httpx.post(url, json=body)
    resp.raise_for_status()
    return normalize_password_reset_response(resp.json())
