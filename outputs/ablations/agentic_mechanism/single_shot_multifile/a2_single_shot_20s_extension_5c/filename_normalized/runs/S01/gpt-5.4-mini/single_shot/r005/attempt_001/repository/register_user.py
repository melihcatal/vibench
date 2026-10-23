import os
import requests
from identity_client import build_identity_base_url, json_headers, normalize_identity_error
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(email: str, password: str, locale: str | None = None, display_name: str | None = None) -> dict:
    base_url = build_identity_base_url()
    payload = RegisterUserRequest(email=email, password=password, locale=locale, display_name=display_name).to_payload()
    response = requests.post(
        f"{base_url}/accounts:signUp",
        headers=json_headers(),
        json=payload,
        timeout=float(os.getenv("IDENTITY_HTTP_TIMEOUT_SECONDS", "20")),
    )
    if response.status_code >= 400:
        raise RuntimeError(normalize_identity_error(response))
    data = response.json()
    return RegisterUserResponse.from_provider(data).to_dict()
