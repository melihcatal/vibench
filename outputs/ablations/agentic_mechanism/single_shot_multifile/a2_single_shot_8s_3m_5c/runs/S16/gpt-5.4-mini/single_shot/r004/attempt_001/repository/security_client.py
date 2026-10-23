import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
DEFAULT_SECRET_ID_ENV = "SECRET_ID"


@dataclass(frozen=True)
class SecretsManagerSettings:
    region_name: Optional[str]


@lru_cache(maxsize=1)
def load_settings() -> SecretsManagerSettings:
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV)
    return SecretsManagerSettings(region_name=region)


def create_secrets_manager_client():
    settings = load_settings()
    config = Config(retries={"max_attempts": 3, "mode": "standard"})
    if settings.region_name:
        return boto3.client("secretsmanager", region_name=settings.region_name, config=config)
    return boto3.client("secretsmanager", config=config)


def get_secret_id(secret_id: Optional[str], default_env_var: str = DEFAULT_SECRET_ID_ENV) -> str:
    if secret_id:
        return secret_id
    env_value = os.getenv(default_env_var)
    if env_value:
        return env_value
    raise ValueError(f"Missing secret id; provide it directly or set {default_env_var}")
