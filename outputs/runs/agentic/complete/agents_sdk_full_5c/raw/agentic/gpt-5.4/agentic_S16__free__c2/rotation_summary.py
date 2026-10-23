from __future__ import annotations

from security_client import build_secret_name, get_secrets_manager_client
from security_models import RotationSummary


ROTATION_SECRET_NAME = build_secret_name("service/rotating_token")


def summarize_rotation(secret_id: str = ROTATION_SECRET_NAME) -> RotationSummary:
    client = get_secrets_manager_client()
    response = client.describe_secret(SecretId=secret_id)
    version_ids = response.get("VersionIdsToStages", {})
    current_version = None
    pending_version = None
    stage_map: dict[str, str] = {}

    for version_id, stages in version_ids.items():
        for stage in stages:
            stage_map[stage] = version_id
            if stage == "AWSCURRENT":
                current_version = version_id
            elif stage == "AWSPENDING":
                pending_version = version_id

    return RotationSummary(
        secret_name=response.get("Name", secret_id),
        current_version=current_version,
        pending_version=pending_version,
        stages=stage_map,
    )
