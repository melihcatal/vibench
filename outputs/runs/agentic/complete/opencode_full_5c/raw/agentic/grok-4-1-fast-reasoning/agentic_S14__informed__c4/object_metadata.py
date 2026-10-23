import boto3
from typing import Dict, Any, Optional
from storage_client import get_aws_client_kwargs
from storage_models import ObjectMetadata


def object_metadata(bucket: str, key: str) -> ObjectMetadata:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)
    response = s3_client.head_object(Bucket=bucket, Key=key)
    return {
        "key": key,
        "size": response["ContentLength"],
        "etag": response["ETag"].strip('"'),
        "last_modified": response["LastModified"].isoformat(),
        "content_type": response.get("ContentType"),
        "metadata": dict(response.get("Metadata", {})),
    }
