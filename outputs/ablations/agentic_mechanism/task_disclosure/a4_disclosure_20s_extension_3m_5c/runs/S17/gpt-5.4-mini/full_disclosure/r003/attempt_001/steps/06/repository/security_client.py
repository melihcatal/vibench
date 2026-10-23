import os
from dataclasses import dataclass
from typing import Optional

import boto3


AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"
AWS_KMS_KEY_ID_ENV = "AWS_KMS_KEY_ID"
AWS_KMS_ENDPOINT_URL_ENV = "AWS_KMS_ENDPOINT_URL"


@dataclass(frozen=True)
class SecurityConfig:
    region_name: Optional[str]
    key_id: Optional[str]
    endpoint_url: Optional[str]


def load_security_config() -> SecurityConfig:
    region_name = os.environ.get(AWS_REGION_ENV) or os.environ.get(AWS_DEFAULT_REGION_ENV)
    key_id = os.environ.get(AWS_KMS_KEY_ID_ENV)
    endpoint_url = os.environ.get(AWS_KMS_ENDPOINT_URL_ENV)
    return SecurityConfig(region_name=region_name, key_id=key_id, endpoint_url=endpoint_url)


def get_kms_client(region_name: Optional[str] = None, endpoint_url: Optional[str] = None):
    config = load_security_config()
    session = boto3.session.Session(region_name=region_name or config.region_name)
    return session.client("kms", endpoint_url=endpoint_url or config.endpoint_url)


def resolve_key_id(key_id: Optional[str] = None) -> Optional[str]:
    return key_id or load_security_config().key_id


def security_headers() -> dict[str, str]:
    config = load_security_config()
    headers = {"x-security-provider": "aws_kms"}
    if config.region_name:
        headers["x-aws-region"] = config.region_name
    if config.key_id:
        headers["x-kms-key-id"] = config.key_id
    return headers
