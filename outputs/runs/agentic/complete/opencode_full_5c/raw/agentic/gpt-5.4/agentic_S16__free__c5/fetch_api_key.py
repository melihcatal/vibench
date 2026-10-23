from __future__ import annotations

from security_client import access_secret, default_project_id
from security_models import SecretRequest


def fetch_api_key(secret_id: str, project_id: str | None = None) -> str:
    request = SecretRequest(
        project_id=project_id or default_project_id(),
        secret_id=secret_id,
        version_id="latest",
    )
    parsed = access_secret(request)
    return parsed.value
