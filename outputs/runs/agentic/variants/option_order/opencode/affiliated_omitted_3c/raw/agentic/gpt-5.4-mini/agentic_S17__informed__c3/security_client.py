import os
from typing import Dict, Optional

import boto3


AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))


def get_kms_client(region_name: Optional[str] = None):
    return boto3.client("kms", region_name=region_name or AWS_REGION)


def get_config() -> Dict[str, str]:
    return {
        "provider": "AWS KMS",
        "region": AWS_REGION,
        "default_key_id": os.getenv("AWS_KMS_KEY_ID", "alias/security-key"),
        "signing_algorithm": os.getenv(
            "AWS_KMS_SIGNING_ALGORITHM", "RSASSA_PSS_SHA_256"
        ),
    }
