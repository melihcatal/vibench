import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


def storage_config() -> Dict[str, Any]:
    return {
        "region_name": os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1",
        "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
        "signature_version": os.getenv("S3_SIGNATURE_VERSION", "s3v4"),
    }


def storage_client(service_name: str = "s3", region_name: Optional[str] = None):
    cfg = storage_config()
    return boto3.client(
        service_name,
        region_name=region_name or cfg["region_name"],
        endpoint_url=cfg["endpoint_url"],
        config=Config(signature_version=cfg["signature_version"]),
    )


def storage_resource(service_name: str = "s3", region_name: Optional[str] = None):
    cfg = storage_config()
    return boto3.resource(
        service_name,
        region_name=region_name or cfg["region_name"],
        endpoint_url=cfg["endpoint_url"],
        config=Config(signature_version=cfg["signature_version"]),
    )
