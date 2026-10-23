import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass(frozen=True)
class SecretManagerConfig:
    secret_id: str
    region_name: Optional[str] = None
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


def load_secret_manager_config(
    secret_id: Optional[str] = None,
    region_name: Optional[str] = None,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> SecretManagerConfig:
    resolved_secret_id = secret_id or os.environ.get("AWS_SECRET_ID") or os.environ.get("SECRET_ID")
    if not resolved_secret_id:
        raise ValueError("Missing secret identifier")
    resolved_region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    resolved_version_id = version_id or os.environ.get("AWS_SECRET_VERSION_ID") or os.environ.get("SECRET_VERSION_ID")
    resolved_version_stage = version_stage or os.environ.get("AWS_SECRET_VERSION_STAGE") or os.environ.get("SECRET_VERSION_STAGE")
    return SecretManagerConfig(
        secret_id=resolved_secret_id,
        region_name=resolved_region,
        version_id=resolved_version_id,
        version_stage=resolved_version_stage,
    )


def create_secretsmanager_client(region_name: Optional[str] = None):
    session = boto3.session.Session(region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    return session.client("secretsmanager")


def get_secret_value(secret_id: Optional[str] = None, region_name: Optional[str] = None, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> str:
    config = load_secret_manager_config(secret_id=secret_id, region_name=region_name, version_id=version_id, version_stage=version_stage)
    client = create_secretsmanager_client(config.region_name)
    params = {"SecretId": config.secret_id}
    if config.version_id:
        params["VersionId"] = config.version_id
    if config.version_stage:
        params["VersionStage"] = config.version_stage
    response = client.get_secret_value(**params)
    secret_string = response.get("SecretString")
    if secret_string is not None:
        return secret_string
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        raise ValueError("Secret does not contain a retrievable value")
    return secret_binary.decode("utf-8")
