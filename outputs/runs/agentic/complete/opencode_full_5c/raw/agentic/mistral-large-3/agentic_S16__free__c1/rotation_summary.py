from security_client import SecretManagerClient
from security_models import SecretRotationSummary
from typing import Optional


def rotation_summary(secret_id: str) -> SecretRotationSummary:
    client = SecretManagerClient()
    versions = client.list_secret_versions(secret_id)
    current_version = versions[0] if versions else None
    previous_version = versions[1] if len(versions) > 1 else None

    latest_data = client.get_secret_with_metadata(secret_id, current_version)

    return SecretRotationSummary(
        secret_id=secret_id,
        current_version=current_version,
        previous_version=previous_version,
        rotation_time=latest_data["create_time"].isoformat(),
        status=latest_data["state"],
    )
