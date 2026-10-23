from __future__ import annotations

from security_client import (
    build_secret_manager_client,
    build_secret_version_name,
    get_project_id,
)
from security_models import SecretPayload, decode_secret_bytes


def fetch_db_secret(
    secret_id: str, project_id: str | None = None, version_id: str = "latest"
) -> SecretPayload:
    client = build_secret_manager_client()
    resolved_project_id = get_project_id(project_id)
    version_name = build_secret_version_name(resolved_project_id, secret_id, version_id)
    access_response = client.access_secret_version(request={"name": version_name})
    secret_response = client.get_secret(
        request={"name": f"projects/{resolved_project_id}/secrets/{secret_id}"}
    )
    return SecretPayload(
        name=version_name,
        value=decode_secret_bytes(access_response.payload.data),
        version_id=version_name.rsplit("/", 1)[-1],
        labels=dict(secret_response.labels),
        metadata={"replication": str(secret_response.replication)},
    )
