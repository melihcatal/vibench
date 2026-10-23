from __future__ import annotations

import os
from typing import Dict

import boto3

from security_models import RotationStatus

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_SECRET_ID = os.getenv("ROTATION_SUMMARY_SECRET_ID", "prod/rotation-summary")


def summarize_rotation_status() -> Dict[str, str]:
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    metadata = client.describe_secret(SecretId=AWS_SECRET_ID)
    current_version = None
    pending_version = None
    version_ids_to_stages = metadata.get("VersionIdsToStages", {}) or {}
    for version_id, stages in version_ids_to_stages.items():
        stages_set = set(stages or [])
        if "AWSCURRENT" in stages_set:
            current_version = version_id
        if "AWSPENDING" in stages_set:
            pending_version = version_id
    status = "rotating" if pending_version else "stable"
    summary = RotationStatus(secret_id=AWS_SECRET_ID, current_version=current_version, pending_version=pending_version, status=status)
    return {"secret_id": summary.secret_id, "current_version": summary.current_version or "", "pending_version": summary.pending_version or "", "status": summary.status}
