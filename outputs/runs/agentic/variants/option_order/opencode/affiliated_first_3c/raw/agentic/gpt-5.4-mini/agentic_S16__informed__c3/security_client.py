import os
from typing import Optional

import boto3
from botocore.client import BaseClient


def get_secret_name(default: str) -> str:
    return os.environ.get("SECRET_NAME", default)


def get_region() -> Optional[str]:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")


def create_secrets_manager_client() -> BaseClient:
    session = boto3.session.Session(region_name=get_region())
    return session.client("secretsmanager")
