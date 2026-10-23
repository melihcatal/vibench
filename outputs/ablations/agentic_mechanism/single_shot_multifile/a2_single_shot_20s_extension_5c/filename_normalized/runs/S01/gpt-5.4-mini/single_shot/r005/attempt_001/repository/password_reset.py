import os
import requests
from identity_client import build_identity_base_url, json_headers, normalize_identity_error
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str, locale: str | None = None) -> dict:
    base_url = build_identity_base_url()
    payload = PasswordResetRequest(email=email, locale=locale).to_payload()
    response = requests.post(
        f"{base_url}/accounts:sendOobCode",
        headers=json_headers(),
        json=payload,
        timeout=float(os.getenv("IDENTITY_HTTP_TIMEOUT_SECONDS", "20")),
    )
    if response.status_code >= 400:
        raise RuntimeError(normalize_identity_error(response))
    return PasswordResetResponse.from_provider(response.json()).to_dict()
