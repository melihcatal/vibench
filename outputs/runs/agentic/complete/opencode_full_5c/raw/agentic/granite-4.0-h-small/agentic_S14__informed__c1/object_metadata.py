# object_metadata.py
# Retrieves metadata/head information for an S3 object

import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ObjectMetadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    """Return metadata for the specified S3 object."""
    client = get_s3_client()
    try:
        response = client.head_object(Bucket=bucket, Key=key)
    except ClientError as exc:
        raise RuntimeError(
            f"Metadata retrieval failed for s3://{bucket}/{key}: {exc}"
        ) from exc
    return ObjectMetadata(response)


# Example usage:
# meta = get_object_metadata("my-bucket", "path/to/file.txt")
# print(meta)
