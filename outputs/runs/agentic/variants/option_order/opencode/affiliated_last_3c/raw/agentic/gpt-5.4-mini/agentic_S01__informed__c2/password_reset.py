import requests

from identity_client import auth0_headers, get_auth0_client_id, get_auth0_domain
from identity_models import PasswordResetRequest


def password_reset(email: str):
    req = PasswordResetRequest(email=email)
    response = requests.post(
        f"https://{get_auth0_domain()}/dbconnections/change_password",
        headers=auth0_headers(),
        json={
            "client_id": get_auth0_client_id(),
            "email": req.as_dict()["email"],
            "connection": "Username-Password-Authentication",
        },
        timeout=30,
    )
    return response.text
