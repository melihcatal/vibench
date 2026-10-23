from __future__ import annotations

from security_client import (
    build_secret_manager_client,
    build_secret_name,
    get_project_id,
)
from security_models import RotationSummary, enabled_version_numbers, normalize_labels


def rotation_summary(secret_id: str, project_id: str | None = None) -> RotationSummary:
    client = build_secret_manager_client()
    resolved_project_id = get_project_id(project_id)
    secret_name = build_secret_name(resolved_project_id, secret_id)
    secret = client.get_secret(request={"name": secret_name})
    versions = list(client.list_secret_versions(request={"parent": secret_name}))
    enabled_versions = enabled_version_numbers(versions)
    return RotationSummary(
        secret_name=secret.name,
        version_count=len(versions),
        latest_enabled_version=enabled_versions[-1] if enabled_versions else None,
        has_scheduled_rotation=bool(secret.rotation.next_rotation_time),
        labels=normalize_labels(secret.labels),
    )
