import os
from dataclasses import dataclass

import boto3


@dataclass
class SecurityClientConfig:
    region_name: str
    kms_key_id: str
    signing_key_id: str | None


def load_security_client_config() -> SecurityClientConfig:
    return SecurityClientConfig(
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        kms_key_id=os.getenv("AWS_KMS_KEY_ID", "alias/key-management"),
        signing_key_id=os.getenv("AWS_KMS_SIGNING_KEY_ID"),
    )


def build_kms_client():
    config = load_security_client_config()
    return boto3.client("kms", region_name=config.region_name)


def get_kms_key_id() -> str:
    return load_security_client_config().kms_key_id


def get_signing_key_id() -> str | None:
    return load_security_client_config().signing_key_id
