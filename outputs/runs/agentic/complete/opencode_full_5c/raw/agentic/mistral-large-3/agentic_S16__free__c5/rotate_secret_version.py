from security_client import SecretManagerClient
from security_models import SecretResponse, normalize_secret_response
import os


def rotate_secret_version(secret_id: str, version_id: str = None) -> SecretResponse:
    client = SecretManagerClient()

    if version_id is None:
        versions = client.list_secret_versions(secret_id)
        version_id = versions[0] if versions else "latest"

    secret_value = client.get_secret_version(secret_id, version_id)

    return normalize_secret_response(
        secret_id=secret_id,
        version_id=version_id,
        secret_value=secret_value,
        labels={"provider": "google-cloud-secret-manager", "rotation": "enabled"},
    )
