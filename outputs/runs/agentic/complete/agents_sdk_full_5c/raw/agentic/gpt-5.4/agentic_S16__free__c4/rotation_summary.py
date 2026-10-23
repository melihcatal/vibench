from __future__ import annotations

from typing import Optional

from google.cloud.secretmanager_v1.types import SecretVersion

from security_client import get_secret_metadata, get_secret_version_metadata
from security_models import RotationSummary, normalize_labels, safe_text


def rotation_summary(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None) -> RotationSummary:
    secret = get_secret_metadata(secret_id=secret_id, project_id=project_id)
    version = get_secret_version_metadata(secret_id=secret_id, version_id=version_id, project_id=project_id)
    topics = [t.name for t in getattr(secret, "topics", [])]
    notes = "; ".join(topics) if topics else safe_text(getattr(secret, "name", ""))
    return RotationSummary(
        secret_name=secret.name,
        version_name=version.name,
        state=SecretVersion.State(version.state).name,
        labels=normalize_labels(secret.labels),
        notes=notes,
    )
