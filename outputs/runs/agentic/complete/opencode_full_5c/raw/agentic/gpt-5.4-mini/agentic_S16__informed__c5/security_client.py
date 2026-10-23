import os
from typing import Optional

import boto3

from security_models import normalize_secret_name, normalize_stage


def build_secrets_client(region_name: Optional[str] = None):
    return boto3.client(
        "secretsmanager", region_name=region_name or os.getenv("AWS_REGION")
    )


def default_secret_id(name: str) -> str:
    return normalize_secret_name(name)


def default_stage(stage: Optional[str]) -> str:
    return normalize_stage(stage)
