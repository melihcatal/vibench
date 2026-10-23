from typing import Optional

import boto3
from botocore.config import Config


def get_secrets_manager_client(region_name: Optional[str] = "us-east-1"):
    config = Config(
        region_name=region_name,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    return boto3.client(service_name="secretsmanager", config=config)
