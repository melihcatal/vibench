from __future__ import annotations

from google.cloud import secretmanager

from security_client import get_gcp_project_id, secret_manager_client
from security_models import RotationSummary, normalize_labels, normalize_rotation_state


def summarize_rotation(
    secret_id: str, project_id: str | None = None
) -> RotationSummary:
    project = get_gcp_project_id(project_id)
    client = secret_manager_client()
    secret_name = f"projects/{project}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": secret_name})
    versions = list(client.list_secret_versions(request={"parent": secret_name}))
    latest = (
        max(versions, key=lambda item: int(item.name.rsplit("/", 1)[-1]))
        if versions
        else None
    )
    state = normalize_rotation_state(
        latest.state if latest else secretmanager.SecretVersion.State.STATE_UNSPECIFIED
    )
    labels = normalize_labels(secret.labels)
    next_rotation = None
    if secret.rotation and secret.rotation.next_rotation_time:
        next_rotation = secret.rotation.next_rotation_time.isoformat()
    return RotationSummary(
        secret_name=secret.name,
        latest_version=latest.name.rsplit("/", 1)[-1] if latest else "",
        state=state,
        label_count=len(labels),
        next_rotation_time=next_rotation,
        notes=f"Google Secret Manager rotation status for {secret.replication.__class__.__name__}",
    )
