import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class SecurityConfig:
    region_name: str
    kms_key_id: Optional[str]
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_session_token: Optional[str]


def load_security_config() -> SecurityConfig:
    return SecurityConfig(
        region_name=os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1')),
        kms_key_id=os.getenv('AWS_KMS_KEY_ID'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    )


def create_kms_client(config: Optional[SecurityConfig] = None):
    config = config or load_security_config()
    kwargs = {'region_name': config.region_name}
    if config.aws_access_key_id and config.aws_secret_access_key:
        kwargs['aws_access_key_id'] = config.aws_access_key_id
        kwargs['aws_secret_access_key'] = config.aws_secret_access_key
    if config.aws_session_token:
        kwargs['aws_session_token'] = config.aws_session_token
    return boto3.client('kms', **kwargs)
