import os
import requests
from identity_client import IdentityClient

def password_reset(email: str, callback_url: str = None):
    """Initiate a password reset flow for an email address on Auth0.

    Sends a password change email to the user.  If `callback_url` is provided,
    the password change will be enforced on redirect after the user clicks the link.

    Returns the Auth0 success response or raises on API error.
    """
    client = IdentityClient()
    body = {
        "client_id": client.auth0_client_id,
        "email": email,
    }
    if callback_url:
        body["result_url"] = callback_url
    response = requests.post(
        f"{client.auth0_domain}/passwordless/start",
        json=body,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
