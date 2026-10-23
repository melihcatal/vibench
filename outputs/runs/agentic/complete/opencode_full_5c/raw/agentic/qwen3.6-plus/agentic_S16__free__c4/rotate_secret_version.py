import os
from security_client import (
    create_secrets_manager_client,
    get_secret_value,
    list_secret_version_ids,
    describe_secret,
)
from security_models import (
    SecretResponse,
    build_aws_secret_request,
    normalize_secret_payload,
)


def rotate_secret_version(
    secret_id: str, version_id: str, region: str = None
) -> SecretResponse:
    request = build_aws_secret_request(secret_id, version_id=version_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_id=request.version_id,
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    return response


def get_staged_secret(
    secret_id: str, stage: str = "AWSPENDING", region: str = None
) -> SecretResponse:
    request = build_aws_secret_request(secret_id, version_stage=stage, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_stage=stage,
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    return response


def list_secret_versions(secret_id: str, region: str = None) -> list:
    client = create_secrets_manager_client(region=region)
    response = list_secret_version_ids(client, secret_id, include_deprecated=False)
    versions = response.get("Versions", [])
    return [
        {
            "version_id": v.get("VersionId", ""),
            "version_stages": v.get("VersionStages", []),
            "created_date": str(v.get("CreatedDate", "")),
            "is_deprecated": v.get("Deprecated", False),
        }
        for v in versions
    ]


def get_secret_with_version_info(
    secret_id: str, version_id: str, region: str = None
) -> dict:
    secret_response = rotate_secret_version(secret_id, version_id, region=region)
    parsed_value = normalize_secret_payload(secret_response.secret_value)
    return {
        "secret_id": secret_response.secret_id,
        "version_id": secret_response.version_id,
        "version_stage": secret_response.version_stage,
        "parsed_value": parsed_value,
        "metadata": secret_response.metadata,
    }


if __name__ == "__main__":
    target_secret_id = os.environ.get("ROTATION_SECRET_ID", "prod/api/payment-key")
    target_version = os.environ.get("TARGET_VERSION_ID", "")
    if target_version:
        result = get_secret_with_version_info(target_secret_id, target_version)
        print(result)
    else:
        versions = list_secret_versions(target_secret_id)
        print(versions)
