import os
import requests
from identity_client import Auth0Client
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    client = Auth0Client()
    url = f"https://{client.domain}/oauth/token"
    payload = LoginRequest(
        email=email,
        password=password,
        client_id=client.client_id,
        audience=client.audience,
    ).dict()
    payload["grant_type"] = "http://auth0.com/oauth/grant-type/password-realm"
    payload["realm"] = client.connection
    payload["scope"] = "openid profile email offline_access"

    response = requests.post(url, json=payload, headers=client.headers)
    response.raise_for_status()
    data = response.json()

    return LoginResponse(**data)
