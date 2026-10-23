from __future__ import annotations

from security_client import safe_get_secret
from security_models import RotationSummary

# AWS Secrets Manager integration
SECRET_ID = "app/rotation/summary"


def rotation_summary() -> RotationSummary:
    response = safe_get_secret(SECRET_ID, version_stage="AWSCURRENT")
    return RotationSummary(
        secret_id=SECRET_ID,
        current_version=response.get("VersionId"),
        previous_version=None,
        labels=list(response.get("VersionStages", [])),
    )
