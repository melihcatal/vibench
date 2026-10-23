import os
import json
import logging
from typing import Optional

import boto3
from botocore.config import Config

from security_models import (
    SecretRequest,
    SecretResponse,
    RotationStatus,
    normalize_aws_secret_response,
    normalize_aws_rotation_response,
    normalize_aws_describe_response,
)

logger = logging.getLogger(__name__)

AWS_SECRETS_MANAGER_ENDPOINT = "https://secretsmanager.{region}.amazonaws.com"


def load_aws_config() -> dict:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN"),
        "region_name": os.environ.get(
            "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
        ),
    }


def get_secrets_manager_client(region: Optional[str] = None) -> boto3.client:
    config = load_aws_config()
    region_name = region or config["region_name"]

    session = boto3.Session(
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        aws_session_token=config["aws_session_token"],
        region_name=region_name,
    )

    client_config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        user_agent_extra="SecretMgmtIntegration/1.0",
    )

    return session.client("secretsmanager", config=client_config)


def fetch_secret_value(request: SecretRequest) -> SecretResponse:
    client = get_secrets_manager_client(request.region)

    kwargs = {
        "SecretId": request.secret_id,
    }

    if request.version_id:
        kwargs["VersionId"] = request.version_id
    elif request.version_stage:
        kwargs["VersionStage"] = request.version_stage

    response = client.get_secret_value(**kwargs)
    return normalize_aws_secret_response(response)


def describe_secret(secret_id: str, region: Optional[str] = None) -> dict:
    client = get_secrets_manager_client(region)
    response = client.describe_secret(SecretId=secret_id)
    return normalize_aws_describe_response(response)


def get_rotation_status(secret_id: str, region: Optional[str] = None) -> RotationStatus:
    client = get_secrets_manager_client(region)
    response = client.describe_secret(SecretId=secret_id)
    return normalize_aws_rotation_response(response)


def list_secret_versions(secret_id: str, region: Optional[str] = None) -> dict:
    client = get_secrets_manager_client(region)
    response = client.describe_secret(SecretId=secret_id)
    return response.get("VersionIdsToStages", {})
