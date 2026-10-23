from __future__ import annotations

from google.cloud import secretmanager

from security_client import get_gcp_project_id, get_secret_manager_client
from security_models import (
    SecretPayload,
    decode_secret_bytes,
    normalize_secret_resource,
)


def read_secret_version(
    secret_id: str, version_id: str = "latest", project_id: str | None = None
) -> SecretPayload:
    resolved_project = project_id or get_gcp_project_id()
    client = get_secret_manager_client()
    name = normalize_secret_resource(resolved_project, secret_id, version_id)
    response = client.access_secret_version(request={"name": name})
    return SecretPayload(
        project_id=resolved_project,
        secret_id=secret_id,
        version_id=version_id,
        value=decode_secret_bytes(response.payload.data),
        data={"provider": "google-cloud-secret-manager", "resource": name},
    )


def read_staged_secret_value(
    secret_id: str,
    stage: str = secretmanager.SecretVersion.State.ENABLED.name,
    project_id: str | None = None,
) -> SecretPayload:
    resolved_project = project_id or get_gcp_project_id()
    client = get_secret_manager_client()
    parent = f"projects/{resolved_project}/secrets/{secret_id}"
    versions = client.list_secret_versions(request={"parent": parent})
    for version in versions:
        current_state = getattr(version.state, "name", str(version.state))
        if current_state == stage:
            version_id = version.name.rsplit("/", 1)[-1]
            return read_secret_version(
                secret_id=secret_id, version_id=version_id, project_id=resolved_project
            )
    raise ValueError(f"No secret version found for stage/state {stage}")
