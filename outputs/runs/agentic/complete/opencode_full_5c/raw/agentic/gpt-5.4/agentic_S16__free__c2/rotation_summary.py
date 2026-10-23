from __future__ import annotations

from security_client import get_secret_metadata, get_secret_version_metadata
from security_models import RotationSummary, normalize_rotation_state


def rotation_summary(
    secret_id: str, version_id: str = "latest", project_id: str | None = None
) -> RotationSummary:
    secret = get_secret_metadata(secret_id=secret_id, project_id=project_id)
    version = get_secret_version_metadata(
        secret_id=secret_id, version_id=version_id, project_id=project_id
    )
    labels = dict(getattr(secret, "labels", {}) or {})
    state = normalize_rotation_state(version.state)
    return RotationSummary(
        secret_id=secret_id,
        version_id=version_id,
        state=state,
        enabled=state == "ENABLED",
        labels=labels,
    )
