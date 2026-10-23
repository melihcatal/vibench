import os
from security_client import SecretManagerClient
from security_models import SecretPayload, Secret


def rotate_secret_version(
    secret_id: str, new_secret_value: str, project_id: str = None
) -> str:
    client = SecretManagerClient(project_id=project_id)
    # Add a new version
    new_version_name = client.add_secret_version(
        secret_id=secret_id, payload_data=new_secret_value.encode("utf-8")
    )
    return new_version_name


def access_specific_secret_version(
    secret_id: str, version_id: str, project_id: str = None
) -> Secret:
    client = SecretManagerClient(project_id=project_id)
    secret_version = client.access_secret_version(
        secret_id=secret_id, version_id=version_id
    )
    return secret_version
