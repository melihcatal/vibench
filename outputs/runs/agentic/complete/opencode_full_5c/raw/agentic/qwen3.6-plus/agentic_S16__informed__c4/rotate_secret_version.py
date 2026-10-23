import os
from typing import Optional
from security_client import (
    build_secret_request,
    fetch_secret,
    list_secret_versions,
    get_secrets_manager_client,
)
from security_models import SecretResponse


def rotate_secret_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> SecretResponse:
    if version_id:
        request = build_secret_request(
            secret_name=secret_name,
            version_id=version_id,
            region=region,
        )
    elif version_stage:
        request = build_secret_request(
            secret_name=secret_name,
            version_stage=version_stage,
            region=region,
        )
    else:
        request = build_secret_request(
            secret_name=secret_name,
            version_stage="AWSPENDING",
            region=region,
        )
    return fetch_secret(request)


def get_staged_secret(
    secret_name: str, stage: str = "AWSPENDING", region: str = None
) -> SecretResponse:
    return rotate_secret_version(secret_name, version_stage=stage, region=region)


def list_available_versions(secret_name: str, region: str = None) -> list[dict]:
    return list_secret_versions(secret_name, region)


def get_version_by_stage(
    secret_name: str, stage: str, region: str = None
) -> Optional[str]:
    versions = list_available_versions(secret_name, region)
    for v in versions:
        if stage in v.get("VersionStages", []):
            return v["VersionId"]
    return None
