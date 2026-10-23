import os
import boto3
from botocore.config import Config
from typing import Optional

from security_models import (
    SecretRequest,
    SecretResponse,
    RotationStatus,
    normalize_secret_response,
    normalize_rotation_status,
)


def get_aws_credentials() -> dict:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN"),
    }


def get_secrets_manager_client(region: Optional[str] = None):
    aws_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    credentials = get_aws_credentials()
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        user_agent_extra="SecretMgmtIntegration/1.0",
    )
    return boto3.client(
        "secretsmanager",
        region_name=aws_region,
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        aws_session_token=credentials["aws_session_token"],
        config=config,
    )


def fetch_secret(request: SecretRequest) -> SecretResponse:
    client = get_secrets_manager_client(request.region)
    kwargs = {"SecretId": request.secret_name}
    if request.version_id:
        kwargs["VersionId"] = request.version_id
    if request.version_stage:
        kwargs["VersionStage"] = request.version_stage
    response = client.get_secret_value(**kwargs)
    return normalize_secret_response(response)


def describe_secret(secret_name: str, region: Optional[str] = None) -> dict:
    client = get_secrets_manager_client(region)
    return client.describe_secret(SecretId=secret_name)


def get_rotation_status(
    secret_name: str, region: Optional[str] = None
) -> RotationStatus:
    client = get_secrets_manager_client(region)
    response = client.describe_secret(SecretId=secret_name)
    return normalize_rotation_status(response)


def list_secret_versions(secret_name: str, region: Optional[str] = None) -> list[dict]:
    client = get_secrets_manager_client(region)
    response = client.list_secret_version_ids(
        SecretId=secret_name, IncludeDeprecated=True
    )
    return response.get("Versions", [])


def build_secret_request(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> SecretRequest:
    return SecretRequest(
        secret_name=secret_name,
        version_id=version_id,
        version_stage=version_stage,
        region=region,
    )
