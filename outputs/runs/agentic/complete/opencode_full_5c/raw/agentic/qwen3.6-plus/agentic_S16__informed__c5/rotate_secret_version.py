import os
from security_models import RotationStatus
from security_client import fetch_rotation_status, create_secrets_manager_client


def rotate_secret_version(
    secret_id: str,
    version_id: str = None,
    version_stage: str = "AWSPENDING",
    region: str = None,
) -> RotationStatus:
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    client = create_secrets_manager_client(region)
    status = fetch_rotation_status(secret_id, region)
    if version_id:
        try:
            response = client.get_secret_value(
                SecretId=secret_id,
                VersionId=version_id,
                VersionStage=version_stage,
            )
            secret_value = response.get("SecretString", "")
            status.notes = f"Retrieved version {version_id} with stage {version_stage}"
        except client.exceptions.ResourceNotFoundException:
            status.notes = f"Version {version_id} with stage {version_stage} not found"
    if version_stage == "AWSPENDING" and status.pending_version_id:
        status.notes = (
            f"Pending version {status.pending_version_id} is staged for rotation"
        )
    return status


def get_secret_version_value(
    secret_id: str,
    version_id: str,
    region: str = None,
) -> str:
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    client = create_secrets_manager_client(region)
    response = client.get_secret_value(
        SecretId=secret_id,
        VersionId=version_id,
    )
    return response.get("SecretString", "")


def get_staged_secret_value(
    secret_id: str,
    stage: str = "AWSPENDING",
    region: str = None,
) -> str:
    region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    client = create_secrets_manager_client(region)
    response = client.get_secret_value(
        SecretId=secret_id,
        VersionStage=stage,
    )
    return response.get("SecretString", "")


if __name__ == "__main__":
    secret_id = os.environ.get("ROTATION_SECRET_ID", "prod/database/postgres-primary")
    result = rotate_secret_version(secret_id)
    print(f"Rotation status for: {result.secret_id}")
    print(f"Rotation enabled: {result.rotation_enabled}")
    print(f"Current version: {result.current_version_id}")
    print(f"Pending version: {result.pending_version_id}")
    print(f"Notes: {result.notes}")
