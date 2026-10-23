from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import normalize_secret_value

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"


def get_secret_client(service_name: str = "secretsmanager", region_name: Optional[str] = None):
    region = region_name or os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV)
    return boto3.client(service_name, region_name=region)


def build_secret_id(name: str) -> str:
    return normalize_secret_value(name).strip()


def fetch_secret_string(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_secret_client(region_name=region_name)
    kwargs: Dict[str, Any] = {"SecretId": build_secret_id(secret_id)}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage

    response = client.get_secret_value(**kwargs)
    value = response.get("SecretString")
    if value is None and response.get("SecretBinary") is not None:
        value = response["SecretBinary"].decode("utf-8", errors="replace")
    return {
        "name": secret_id,
        "value": normalize_secret_value(value),
        "version": response.get("VersionId"),
        "metadata": {
            "arn": response.get("ARN"),
            "created_date": response.get("CreatedDate"),
            "version_stages": response.get("VersionStages", []),
        },
    }


def list_secret_versions(secret_id: str, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = get_secret_client(region_name=region_name)
    response = client.list_secret_version_ids(SecretId=build_secret_id(secret_id), IncludeDeprecated=True)
    return response


def safe_json_loads(text: str) -> Any:
    return json.loads(text)


def ensure_aws_credentials_present() -> None:
    if not (os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY")):
        raise RuntimeError("AWS credentials are required for AWS Secrets Manager integration")
