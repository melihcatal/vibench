from __future__ import annotations

import os

from security_client import fetch_secret_string, list_secret_versions, ensure_aws_credentials_present
from security_models import RotationSummaryResult


def rotate_secret_version(secret_name: str, version_id: str | None = None, version_stage: str | None = "AWSCURRENT") -> RotationSummaryResult:
    ensure_aws_credentials_present()
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    payload = fetch_secret_string(secret_name, version_id=version_id, version_stage=version_stage, region_name=region)
    versions = list_secret_versions(secret_name, region_name=region)
    staged = []
    for item in versions.get("Versions", []):
        if item.get("VersionStages"):
            staged.append(item.get("VersionId", ""))
    return RotationSummaryResult(
        secret_name=secret_name,
        current_version=payload.get("version"),
        staged_versions=staged,
        status="rotated" if version_id or version_stage else "current",
    )
