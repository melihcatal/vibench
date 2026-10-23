import os
from dataclasses import dataclass
from typing import Optional

import boto3


@dataclass
class SecurityConfig:
    aws_region: str
    kms_key_id: Optional[str]


def load_security_config() -> SecurityConfig:
    return SecurityConfig(aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")), kms_key_id=os.getenv("AWS_KMS_KEY_ID"))


def build_kms_client():
    config = load_security_config()
    return boto3.client("kms", region_name=config.aws_region)


def build_comprehend_client():
    config = load_security_config()
    return boto3.client("comprehend", region_name=config.aws_region)
