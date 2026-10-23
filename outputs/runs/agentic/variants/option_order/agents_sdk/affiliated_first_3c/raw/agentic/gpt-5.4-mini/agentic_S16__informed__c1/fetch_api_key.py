from __future__ import annotations

import os

from security_client import access_secret_text
from security_models import SecretRequest


def fetch_api_key(secret_id: str | None = None) -> str:
    request = SecretRequest(secret_id=secret_id or os.environ.get("API_KEY_SECRET_ID", "api-key"))
    secret = access_secret_text(request.secret_id, version=request.version)
    return secret.value
