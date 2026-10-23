import os
from security_client import (
    fetch_secret,
    get_secrets_manager_client,
    list_secret_versions,
)
from security_models import SecretRequest, SecretResponse


def rotate_secret_version(
    secret_id: str = None, version_id: str = None, version_stage: str = "AWSCURRENT"
) -> SecretResponse:
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    request = SecretRequest(
        secret_id=target_id,
        version_id=version_id,
        version_stage=version_stage,
        with_decryption=True,
    )
    return fetch_secret(request)


def get_staged_secret(
    secret_id: str = None, stage: str = "AWSPENDING"
) -> SecretResponse:
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    request = SecretRequest(
        secret_id=target_id,
        version_stage=stage,
        with_decryption=True,
    )
    return fetch_secret(request)


def get_specific_version(secret_id: str, version_id: str) -> SecretResponse:
    request = SecretRequest(
        secret_id=secret_id,
        version_id=version_id,
        with_decryption=True,
    )
    return fetch_secret(request)


def list_all_versions(secret_id: str = None) -> list:
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    return list_secret_versions(target_id)


def get_version_metadata(secret_id: str = None) -> dict:
    client = get_secrets_manager_client()
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    response = client.describe_secret(SecretId=target_id)
    version_map = response.get("VersionIdsToStages", {})
    versions = list_secret_versions(target_id)
    return {
        "secret_id": target_id,
        "version_ids_to_stages": version_map,
        "versions": [
            {
                "version_id": v.get("VersionId"),
                "stages": v.get("VersionStages", []),
                "created_date": v.get("CreatedDate"),
                "last_accessed_date": v.get("LastAccessedDate"),
            }
            for v in versions
        ],
    }


def move_secret_stage(
    secret_id: str, version_id: str, from_stage: str, to_stage: str
) -> dict:
    client = get_secrets_manager_client()
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    response = client.update_secret_version_stage(
        SecretId=target_id,
        VersionStage=to_stage,
        MoveToVersionId=version_id,
        RemoveFromVersionId=version_id if from_stage else None,
    )
    return response


if __name__ == "__main__":
    metadata = get_version_metadata()
    print(f"Secret: {metadata['secret_id']}")
    for v in metadata["versions"]:
        print(f"  Version: {v['version_id']} - Stages: {v['stages']}")
