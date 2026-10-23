from __future__ import annotations

from security_client import access_secret, default_project_id
from security_models import SecretRequest


def fetch_db_secret(
    secret_id: str, version_id: str = "latest", project_id: str | None = None
) -> str:
    request = SecretRequest(
        project_id=project_id or default_project_id(),
        secret_id=secret_id,
        version_id=version_id,
    )
    parsed = access_secret(request)
    return parsed.value
