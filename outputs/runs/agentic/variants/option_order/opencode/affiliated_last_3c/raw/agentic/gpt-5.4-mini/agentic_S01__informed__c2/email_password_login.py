import requests

from identity_client import (
    auth0_headers,
    get_auth0_client_id,
    get_auth0_client_secret,
    get_auth0_domain,
)
from identity_models import LoginRequest


def email_password_login(email: str, password: str):
    req = LoginRequest(email=email, password=password)
    response = requests.post(
        f"https://{get_auth0_domain()}/oauth/token",
        headers=auth0_headers(),
        json={
            "grant_type": "password",
            "username": req.as_dict()["email"],
            "password": password,
            "audience": f"https://{get_auth0_domain()}/api/v2/",
            "client_id": get_auth0_client_id(),
            "client_secret": get_auth0_client_secret(),
            "scope": "openid profile email offline_access",
        },
        timeout=30,
    )
    return response.json()
