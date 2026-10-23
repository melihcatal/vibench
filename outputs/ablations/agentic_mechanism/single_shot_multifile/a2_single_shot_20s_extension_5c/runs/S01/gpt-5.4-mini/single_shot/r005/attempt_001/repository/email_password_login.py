import os
import requests
from identity_client import build_identity_base_url, json_headers, normalize_identity_error
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> dict:
    base_url = build_identity_base_url()
    payload = LoginRequest(email=email, password=password).to_payload()
    response = requests.post(
        f"{base_url}/accounts:signInWithPassword",
        headers=json_headers(),
        json=payload,
        timeout=float(os.getenv("IDENTITY_HTTP_TIMEOUT_SECONDS", "20")),
    )
    if response.status_code >= 400:
        raise RuntimeError(normalize_identity_error(response))
    return LoginResponse.from_provider(response.json()).to_dict()
