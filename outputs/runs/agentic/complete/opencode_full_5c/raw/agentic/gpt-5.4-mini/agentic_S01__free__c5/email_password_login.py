import requests

from identity_client import auth0_url, load_identity_config, normalize_email
from identity_models import LoginRequest, extract_tokens, to_payload


def login(email: str, password: str):
    config = load_identity_config()
    payload = to_payload(
        LoginRequest(
            email=normalize_email(email),
            password=password,
            realm=config.auth0_connection,
        )
    )
    response = requests.post(
        auth0_url(config.auth0_domain, "/oauth/token"),
        json={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": payload["email"],
            "password": payload["password"],
            "realm": payload["realm"],
            "client_id": config.auth0_client_id,
            "client_secret": config.auth0_client_secret,
            "audience": config.auth0_audience,
            "scope": "openid profile email offline_access",
        },
        timeout=30,
    )
    response.raise_for_status()
    return extract_tokens(response.json())
