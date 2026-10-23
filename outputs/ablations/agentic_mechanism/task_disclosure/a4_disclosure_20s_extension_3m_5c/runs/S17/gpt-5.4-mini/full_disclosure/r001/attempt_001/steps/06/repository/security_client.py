import os
from dataclasses import dataclass
from typing import Optional

from boto3.session import Session


@dataclass(frozen=True)
class SecurityConfig:
    region_name: str
    key_arn: Optional[str]
    encryption_context: dict[str, str]


def load_security_config() -> SecurityConfig:
    region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    key_arn = os.getenv("AWS_KMS_KEY_ARN") or os.getenv("KMS_KEY_ARN")
    encryption_context_raw = os.getenv("AWS_KMS_ENCRYPTION_CONTEXT", "")
    encryption_context: dict[str, str] = {}
    if encryption_context_raw:
        for item in encryption_context_raw.split(","):
            if "=" in item:
                key, value = item.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key:
                    encryption_context[key] = value
    return SecurityConfig(region_name=region_name, key_arn=key_arn, encryption_context=encryption_context)


def create_session(config: Optional[SecurityConfig] = None) -> Session:
    cfg = config or load_security_config()
    return Session(region_name=cfg.region_name)


def create_kms_client(config: Optional[SecurityConfig] = None):
    cfg = config or load_security_config()
    return create_session(cfg).client("kms")


def resolve_key_id(key_id: Optional[str] = None, config: Optional[SecurityConfig] = None) -> str:
    cfg = config or load_security_config()
    resolved = key_id or cfg.key_arn
    if not resolved:
        raise ValueError("A managed key identifier is required via key_id or AWS_KMS_KEY_ARN")
    return resolved
