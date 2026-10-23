import os

from identity_client import build_client
from identity_models import RegisterUserRequest, as_payload


def register_user(email: str, password: str, locale: str = "en"):
    client = build_client()
    payload = as_payload(
        RegisterUserRequest(email=email, password=password, locale=locale)
    )
    payload["email"] = payload["email"].strip().lower()
    payload["connection"] = os.environ.get(
        "AUTH0_CONNECTION", "Username-Password-Authentication"
    )
    return client.post("/api/v2/users", payload)
