import requests

from identity_client import auth0_base_url, get_session
from identity_models import (
    RegisterUserRequest,
    as_payload,
    normalize_email,
    normalize_locale,
)


def register_user(email: str, password: str, locale: str = "en"):
    req = RegisterUserRequest(
        email=normalize_email(email), password=password, locale=normalize_locale(locale)
    )
    session = get_session()
    response = session.post(
        f"{auth0_base_url()}/dbconnections/signup",
        json={
            "email": req.email,
            "password": req.password,
            "connection": "Username-Password-Authentication",
            "user_metadata": {"locale": req.locale},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
