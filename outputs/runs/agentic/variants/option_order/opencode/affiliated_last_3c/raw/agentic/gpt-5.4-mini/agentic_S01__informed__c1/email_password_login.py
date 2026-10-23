import os

from identity_client import build_client
from identity_models import LoginRequest, as_payload


def email_password_login(email: str, password: str):
    client = build_client()
    payload = as_payload(LoginRequest(email=email, password=password))
    payload["realm"] = os.environ.get("AUTH0_REALM", "Username-Password-Authentication")
    payload["audience"] = os.environ.get("AUTH0_AUDIENCE", "https://example.api")
    return client.post("/oauth/token", payload)
