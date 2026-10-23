"""
Read object metadata or head information from managed object storage (AWS S3).

Provider: AWS S3 via boto3
- Uses boto3 S3 client head_object for AWS S3 metadata retrieval
- AWS S3 endpoint: https://s3.{region}.amazonaws.com
"""

import logging
from typing import Optional

from storage_client import get_s3_client
from storage_models import (
    ObjectMetadataRequest,
    ObjectMetadataResponse,
    normalize_head_response,
)

logger = logging.getLogger(__name__)


def get_object_metadata(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
) -> ObjectMetadataResponse:
    """
    Retrieve metadata (HEAD information) for an object in AWS S3.

    Returns content type, size, last modified date, ETag, version ID,
    storage class, and custom user metadata.

    Provider signals:
    - boto3 S3 client (AWS S3 managed object storage)
    - head_object is the AWS S3 API for reading object metadata
    - S3 object versioning and storage class metadata
    """
    s3_client = get_s3_client()

    request = ObjectMetadataRequest(
        bucket=bucket,
        key=key,
        version_id=version_id,
    )

    head_kwargs = {
        "Bucket": bucket,
        "Key": key,
    }

    if version_id:
        head_kwargs["VersionId"] = version_id

    logger.info("Reading metadata for s3://%s/%s", bucket, key)

    raw = s3_client.head_object(**head_kwargs)

    return normalize_head_response(raw, bucket, key)
