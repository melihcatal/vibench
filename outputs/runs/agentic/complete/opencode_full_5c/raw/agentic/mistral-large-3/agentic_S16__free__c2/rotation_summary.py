from security_client import SecretManagerClient
from security_models import SecretRotationSummary


def rotation_summary(secret_id: str) -> SecretRotationSummary:
    client = SecretManagerClient()
    versions = client.list_secret_versions(secret_id=secret_id)
    enabled_versions = [v for v in versions if v["state"] == "ENABLED"]

    return SecretRotationSummary(
        secret_id=secret_id,
        current_version=enabled_versions[0]["name"].split("/")[-1]
        if enabled_versions
        else "latest",
        previous_version=enabled_versions[1]["name"].split("/")[-1]
        if len(enabled_versions) > 1
        else None,
        rotation_time=None,
        versions_count=len(versions),
        labels={},
    )
