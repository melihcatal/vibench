import os
from functools import lru_cache
from typing import Optional

import boto3
from botocore.client import BaseClient
from botocore.config import Config


def _region_name() -> Optional[str]:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")


def _aws_config() -> Config:
    return Config(retries={"max_attempts": 5, "mode": "standard"})


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    return boto3.client("s3", region_name=_region_name(), config=_aws_config())


def get_bucket_name(explicit: Optional[str] = None) -> str:
    return explicit or os.environ["S3_BUCKET"]


def get_default_prefix(explicit: Optional[str] = None) -> str:
    return explicit or os.getenv("S3_PREFIX", "")
