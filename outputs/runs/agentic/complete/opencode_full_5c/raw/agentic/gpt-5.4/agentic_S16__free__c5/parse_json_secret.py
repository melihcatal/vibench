from __future__ import annotations

from security_client import access_secret, default_project_id
from security_models import SecretRequest, parse_secret_json


def parse_json_secret(
    secret_id: str, version_id: str = "latest", project_id: str | None = None
) -> dict:
    request = SecretRequest(
        project_id=project_id or default_project_id(),
        secret_id=secret_id,
        version_id=version_id,
    )
    parsed = access_secret(request)
    return parse_secret_json(parsed.value)
