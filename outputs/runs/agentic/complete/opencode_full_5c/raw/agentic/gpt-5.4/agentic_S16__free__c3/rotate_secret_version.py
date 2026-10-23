from __future__ import annotations

from security_client import (
    build_secret_manager_client,
    build_secret_version_name,
    get_project_id,
)
from security_models import SecretPayload, decode_secret_bytes


def read_secret_version(
    secret_id: str, version_id: str, project_id: str | None = None
) -> SecretPayload:
    client = build_secret_manager_client()
    resolved_project_id = get_project_id(project_id)
    resource_name = build_secret_version_name(
        resolved_project_id, secret_id, version_id
    )
    response = client.access_secret_version(request={"name": resource_name})
    return SecretPayload(
        name=resource_name,
        value=decode_secret_bytes(response.payload.data),
        version_id=version_id,
        labels={},
        metadata={"provider": "Google Cloud Secret Manager"},
    )
