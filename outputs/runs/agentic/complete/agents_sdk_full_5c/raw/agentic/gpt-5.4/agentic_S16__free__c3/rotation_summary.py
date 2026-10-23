from __future__ import annotations

from typing import Optional

from google.cloud import secretmanager

from security_client import get_project_id, get_secret_manager_client
from security_models import RotationSummary, normalize_labels


DEFAULT_SECRET_ID = "rotating-service-credential"


def summarize_rotation(secret_id: str = DEFAULT_SECRET_ID, project_id: Optional[str] = None) -> RotationSummary:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    resolved_project = get_project_id(project_id)
    secret_name = f"projects/{resolved_project}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": secret_name})
    versions = list(client.list_secret_versions(request={"parent": secret_name}))
    current_version = next((v.name.rsplit("/", 1)[-1] for v in versions if v.state == secretmanager.SecretVersion.State.ENABLED), "none")
    enabled_versions = sum(1 for v in versions if v.state == secretmanager.SecretVersion.State.ENABLED)
    destroyed_versions = sum(1 for v in versions if v.state == secretmanager.SecretVersion.State.DESTROYED)
    return RotationSummary(
        secret_name=secret.name,
        current_version=current_version,
        enabled_versions=enabled_versions,
        destroyed_versions=destroyed_versions,
        labels=normalize_labels(secret.labels),
    )
