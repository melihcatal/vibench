from __future__ import annotations

import os

from security_client import list_secret_versions, ensure_aws_credentials_present
from security_models import RotationSummaryResult


def rotation_summary(secret_name: str) -> RotationSummaryResult:
    ensure_aws_credentials_present()
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    versions = list_secret_versions(secret_name, region_name=region)
    current = None
    staged = []
    for item in versions.get("Versions", []):
        if "AWSCURRENT" in item.get("VersionStages", []):
            current = item.get("VersionId")
        staged.extend(item.get("VersionStages", []))
    return RotationSummaryResult(
        secret_name=secret_name,
        current_version=current,
        staged_versions=sorted(set(staged)),
        status="healthy" if current else "unknown",
    )
