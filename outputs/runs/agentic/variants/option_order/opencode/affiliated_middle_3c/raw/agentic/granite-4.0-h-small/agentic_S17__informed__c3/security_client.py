import os
from typing import Any, Dict, Optional

# Provider selection – example: AWS KMS
# Load credentials from environment variables (provider‑identifying signals)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")


# Simple configuration object for KMS client
class SecurityConfig:
    def __init__(self):
        self.aws_access_key_id = AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        self.kms_key_id = AWS_KMS_KEY_ID


def get_security_config() -> SecurityConfig:
    return SecurityConfig()


# ------------------- SDK client helpers -------------------


def create_kms_client(config: SecurityConfig) -> Any:
    """Creates a boto3 KMS client using credentials from the config."""
    if not config.aws_access_key_id or not config.aws_secret_access_key:
        raise RuntimeError("AWS credentials missing")
    return boto3.client(
        "kms",
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
    )


# Usage example (not executed at import time)
if __name__ == "__main__":
    cfg = get_security_config()
    kms = create_kms_client(cfg)
    print("KMS client version:", kms.meta.service_model.api_version)
