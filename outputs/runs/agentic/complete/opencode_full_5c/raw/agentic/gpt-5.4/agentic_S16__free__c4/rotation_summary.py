from __future__ import annotations

from security_client import get_secret_metadata, get_secret_version
from security_models import RotationSummary, normalize_labels


def rotation_summary(secret_id: str, version_id: str = "latest") -> RotationSummary:
    secret = get_secret_metadata(secret_id)
    version = get_secret_version(secret_id, version_id)
    create_time = version.create_time.isoformat() if version.create_time else ""
    destroy_time = version.destroy_time.isoformat() if version.destroy_time else None
    return RotationSummary(
        secret_name=secret.name,
        version_name=version.name,
        state=version.state.name,
        create_time=create_time,
        destroy_time=destroy_time,
        labels=normalize_labels(secret.labels),
    )
