import os
import requests
from identity_client import build_identity_base_url, json_headers, normalize_identity_error
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(refresh_token: str) -> dict:
    base_url = build_identity_base_url()
    payload = RefreshSessionRequest(refresh_token=refresh_token).to_payload()
    headers = dict(json_headers())
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    response = requests.post(
        f"{base_url}/token",
        headers=headers,
        data=payload,
        timeout=float(os.getenv("IDENTITY_HTTP_TIMEOUT_SECONDS", "20")),
    )
    if response.status_code >= 400:
        raise RuntimeError(normalize_identity_error(response))
    return RefreshSessionResponse.from_provider(response.json()).to_dict()
