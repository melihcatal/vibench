import requests

from identity_client import auth0_url, load_identity_config, normalize_email
from identity_models import RegisterUserRequest, to_payload


def register_user(
    email: str, password: str, given_name: str = None, family_name: str = None
):
    config = load_identity_config()
    payload = to_payload(
        RegisterUserRequest(
            email=normalize_email(email),
            password=password,
            connection=config.auth0_connection,
            given_name=given_name,
            family_name=family_name,
        )
    )
    response = requests.post(
        auth0_url(config.auth0_domain, "/dbconnections/signup"),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
