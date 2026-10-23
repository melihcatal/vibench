import requests

from identity_client import (
    auth0_headers,
    get_auth0_audience,
    get_auth0_client_id,
    get_auth0_client_secret,
    get_auth0_domain,
)
from identity_models import RegistrationRequest


def register_user(
    email: str, password: str, locale: str = "en", full_name: str | None = None
):
    req = RegistrationRequest(
        email=email, password=password, locale=locale, full_name=full_name
    )
    domain = get_auth0_domain()
    token = requests.post(
        f"https://{domain}/oauth/token",
        headers=auth0_headers(),
        json={
            "grant_type": "client_credentials",
            "client_id": get_auth0_client_id(),
            "client_secret": get_auth0_client_secret(),
            "audience": get_auth0_audience() or f"https://{domain}/api/v2/",
        },
        timeout=30,
    ).json()["access_token"]
    response = requests.post(
        f"https://{domain}/api/v2/users",
        headers={**auth0_headers(), "Authorization": f"Bearer {token}"},
        json={"connection": "Username-Password-Authentication", **req.as_dict()},
        timeout=30,
    )
    return response.json()
