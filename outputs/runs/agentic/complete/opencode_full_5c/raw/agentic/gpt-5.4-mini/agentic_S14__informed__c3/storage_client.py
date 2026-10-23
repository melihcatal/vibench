import os
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3


@lru_cache(maxsize=1)
def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION"),
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
    )


def get_bucket_name(default: Optional[str] = None) -> str:
    value = os.environ.get("S3_BUCKET") or os.environ.get("AWS_S3_BUCKET") or default
    if not value:
        raise ValueError("missing S3 bucket name")
    return value


def get_default_kms_key_id() -> Optional[str]:
    return os.environ.get("S3_SSE_KMS_KEY_ID")


def build_put_kwargs(
    content_type: Optional[str] = None, metadata: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {}
    if content_type:
        kwargs["ContentType"] = content_type
    if metadata:
        kwargs["Metadata"] = metadata
    kms_key = get_default_kms_key_id()
    if kms_key:
        kwargs["ServerSideEncryption"] = "aws:kms"
        kwargs["SSEKMSKeyId"] = kms_key
    return kwargs
