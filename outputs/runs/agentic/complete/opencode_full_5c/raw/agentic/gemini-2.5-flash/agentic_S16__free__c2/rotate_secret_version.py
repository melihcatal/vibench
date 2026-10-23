import os
from security_client import SecretManagerClient
from security_models import SecretPayload


def rotate_secret_version(
    secret_id: str = "AWESOME_SECRET", version_id: str = "1"
) -> SecretPayload:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    client = SecretManagerClient(project_id=project_id)
    specific_version_data = client.access_secret(secret_id, version_id=version_id)

    return SecretPayload(name=secret_id, data=specific_version_data, version=version_id)
