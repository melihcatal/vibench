from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional

import boto3
from botocore.config import Config

AWS_SECRETS_MANAGER_ENDPOINT_ENV = "AWS_SECRETS_MANAGER_ENDPOINT"
AWS_REGION_ENV = "AWS_REGION"


@dataclass(frozen=True)
class SecurityClientConfig:
    region_name: str
    endpoint_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_security_client_config() -> SecurityClientConfig:
    return SecurityClientConfig(
        region_name=os.getenv(AWS_REGION_ENV, "us-east-1"),
        endpoint_url=os.getenv(AWS_SECRETS_MANAGER_ENDPOINT_ENV),
    )


@lru_cache(maxsize=1)
def get_aws_secrets_manager_client() -> Any:
    cfg = load_security_client_config()
    return boto3.client(
        "secretsmanager",
        region_name=cfg.region_name,
        endpoint_url=cfg.endpoint_url,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def secret_id_from_env(env_name: str, default: str) -> str:
    return os.getenv(env_name, default)
