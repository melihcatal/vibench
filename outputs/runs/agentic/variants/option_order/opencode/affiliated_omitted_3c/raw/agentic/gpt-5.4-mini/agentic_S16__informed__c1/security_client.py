import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class SecretConfig:
    region_name: str
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


def load_secret_config(
    secret_id: str,
    version_stage: Optional[str] = None,
    version_id: Optional[str] = None,
) -> SecretConfig:
    return SecretConfig(
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
        secret_id=secret_id,
        version_stage=version_stage,
        version_id=version_id,
    )


def secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client(
        "secretsmanager",
        region_name=region_name
        or os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
    )


def fetch_secret_value(client: Any, config: SecretConfig) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {"SecretId": config.secret_id}
    if config.version_stage:
        kwargs["VersionStage"] = config.version_stage
    if config.version_id:
        kwargs["VersionId"] = config.version_id
    return client.get_secret_value(**kwargs)


def secret_string_from_response(response: Dict[str, Any]) -> str:
    value = response.get("SecretString")
    if value is not None:
        return value
    return response["SecretBinary"].decode("utf-8")
