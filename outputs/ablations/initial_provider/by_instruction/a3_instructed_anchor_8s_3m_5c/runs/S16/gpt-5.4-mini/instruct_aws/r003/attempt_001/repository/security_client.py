import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class SecurityConfig:
    region_name: Optional[str] = None
    secrets_endpoint_url: Optional[str] = None


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        region_name=os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        secrets_endpoint_url=os.environ.get("AWS_SECRETSMANAGER_ENDPOINT_URL"),
    )


def build_secrets_client(config: Optional[SecurityConfig] = None):
    cfg = config or load_security_config()
    kwargs: Dict[str, Any] = {}
    if cfg.region_name:
        kwargs["region_name"] = cfg.region_name
    if cfg.secrets_endpoint_url:
        kwargs["endpoint_url"] = cfg.secrets_endpoint_url
    return boto3.client("secretsmanager", **kwargs)


def get_secret_string(client, secret_id: str, version_stage: Optional[str] = None, version_id: Optional[str] = None) -> str:
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    response = client.get_secret_value(**params)
    return response.get("SecretString") or ""
