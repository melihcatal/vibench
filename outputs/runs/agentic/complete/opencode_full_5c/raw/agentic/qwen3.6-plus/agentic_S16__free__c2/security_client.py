import os
import json
import boto3
from botocore.config import Config
from typing import Optional, Dict, Any
from security_models import (
    SecretRequest,
    SecretResponse,
    RotationStatus,
    normalize_secret_value,
    format_secret_tags,
)


AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SECRETS_MANAGER_ENDPOINT = os.environ.get("AWS_SECRETS_MANAGER_ENDPOINT", None)


def get_secrets_manager_client() -> boto3.client:
    config = Config(
        region_name=AWS_REGION,
        retries={"max_attempts": 3, "mode": "standard"},
    )
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    client_kwargs = {"config": config}
    if AWS_SECRETS_MANAGER_ENDPOINT:
        client_kwargs["endpoint_url"] = AWS_SECRETS_MANAGER_ENDPOINT
    return session.client("secretsmanager", **client_kwargs)


def fetch_secret(request: SecretRequest) -> SecretResponse:
    client = get_secrets_manager_client()
    params: Dict[str, Any] = {"SecretId": request.secret_id}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    response = client.get_secret_value(**params)
    secret_value = normalize_secret_value(
        response.get("SecretString") or response.get("SecretBinary", "")
    )
    return SecretResponse(
        secret_id=response.get("Name", request.secret_id),
        secret_value=secret_value,
        version_id=response.get("VersionId"),
        version_stages=response.get("VersionStages", []),
        created_date=response.get("CreatedDate"),
        last_accessed_date=response.get("LastAccessedDate"),
        raw_response=response,
    )


def describe_secret(secret_id: str) -> Dict[str, Any]:
    client = get_secrets_manager_client()
    return client.describe_secret(SecretId=secret_id)


def get_rotation_status(secret_id: str) -> RotationStatus:
    metadata = describe_secret(secret_id)
    rotation_rules = metadata.get("RotationRules", {})
    return RotationStatus(
        secret_id=secret_id,
        rotation_enabled=metadata.get("RotationEnabled", False),
        last_rotated_date=metadata.get("LastRotatedDate"),
        next_rotation_date=metadata.get("NextRotationDate"),
        rotation_lambda_arn=metadata.get("RotationLambdaARN"),
        rotation_rules=rotation_rules,
        current_version=metadata.get("VersionIdsToStages", {}),
    )


def list_secret_versions(secret_id: str) -> list:
    client = get_secrets_manager_client()
    response = client.list_secret_version_ids(SecretId=secret_id)
    return response.get("Versions", [])


def parse_json_secret_value(request: SecretRequest) -> dict:
    response = fetch_secret(request)
    if isinstance(response.secret_value, str):
        return json.loads(response.secret_value)
    if isinstance(response.secret_value, dict):
        return response.secret_value
    raise ValueError(
        f"Secret value is not JSON-parseable: {type(response.secret_value)}"
    )


def get_secret_tags(secret_id: str) -> dict:
    metadata = describe_secret(secret_id)
    return format_secret_tags(metadata.get("Tags", []))
