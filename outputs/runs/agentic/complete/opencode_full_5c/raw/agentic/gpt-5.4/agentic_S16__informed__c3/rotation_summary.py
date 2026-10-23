from __future__ import annotations

from security_client import get_secret_metadata, summarize_text
from security_models import RotationSummary, normalize_rotation_summary


def rotation_summary(secret_id: str) -> dict:
    metadata = get_secret_metadata(secret_id)
    stages = metadata["version_ids_to_stages"]
    current_version = None
    previous_version = None
    for version_id, version_stages in stages.items():
        if "AWSCURRENT" in version_stages:
            current_version = version_id
        if "AWSPREVIOUS" in version_stages:
            previous_version = version_id
    summary = RotationSummary(
        secret_id=secret_id,
        current_version=current_version,
        previous_version=previous_version,
        stages=stages,
        last_rotated_date=metadata.get("last_rotated_date"),
    )
    prompt = (
        f"Summarize the rotation status for AWS Secrets Manager secret {secret_id}. "
        f"Current version: {current_version}. Previous version: {previous_version}. "
        f"Last rotated date: {metadata.get('last_rotated_date')}. "
        f"Stages: {stages}. Respond in 2 concise sentences."
    )
    result = normalize_rotation_summary(summary)
    result["llm_summary"] = summarize_text(prompt)
    return result
