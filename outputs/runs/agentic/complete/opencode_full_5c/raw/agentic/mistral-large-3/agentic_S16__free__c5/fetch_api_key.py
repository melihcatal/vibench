from security_client import SecretManagerClient
from security_models import SecretResponse, normalize_secret_response
import os


def fetch_api_key(secret_id: str = "API_KEY") -> SecretResponse:
    client = SecretManagerClient()
    secret_value = client.get_secret_latest(secret_id)
    version_id = client.list_secret_versions(secret_id)[0]
    return normalize_secret_response(
        secret_id=secret_id,
        version_id=version_id,
        secret_value=secret_value,
        labels={"provider": "google-cloud-secret-manager", "type": "api-key"},
    )
