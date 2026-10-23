from __future__ import annotations

from security_client import default_project_id, get_secret_metadata, get_secret_resource
from security_models import RotationSummary, SecretRequest, normalize_rotation_state


def summarize_rotation(
    secret_id: str, version_id: str = "latest", project_id: str | None = None
) -> dict:
    resolved_project_id = project_id or default_project_id()
    request = SecretRequest(
        project_id=resolved_project_id, secret_id=secret_id, version_id=version_id
    )
    version = get_secret_metadata(request)
    secret = get_secret_resource(secret_id, resolved_project_id)
    summary = RotationSummary(
        secret_name=version.name,
        version=version.name.rsplit("/", 1)[-1],
        state=normalize_rotation_state(version.state),
        labels=dict(secret.labels),
    )
    return {
        "secret_name": summary.secret_name,
        "version": summary.version,
        "state": summary.state,
        "labels": summary.labels,
        "rotation_period_seconds": int(secret.rotation.rotation_period.seconds)
        if secret.rotation and secret.rotation.rotation_period
        else 0,
        "next_rotation_time": secret.next_rotation_time.isoformat()
        if secret.next_rotation_time
        else None,
    }
