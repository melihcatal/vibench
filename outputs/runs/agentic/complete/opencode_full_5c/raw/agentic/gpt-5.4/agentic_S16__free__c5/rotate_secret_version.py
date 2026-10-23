from __future__ import annotations

from security_client import access_secret, default_project_id, get_secret_metadata
from security_models import SecretRequest, normalize_rotation_state


def read_secret_version(
    secret_id: str, version_id: str, project_id: str | None = None
) -> dict:
    request = SecretRequest(
        project_id=project_id or default_project_id(),
        secret_id=secret_id,
        version_id=version_id,
    )
    parsed = access_secret(request)
    metadata = get_secret_metadata(request)
    return {
        "name": parsed.name,
        "version": version_id,
        "value": parsed.value,
        "state": normalize_rotation_state(metadata.state),
        "etag": metadata.etag,
    }
