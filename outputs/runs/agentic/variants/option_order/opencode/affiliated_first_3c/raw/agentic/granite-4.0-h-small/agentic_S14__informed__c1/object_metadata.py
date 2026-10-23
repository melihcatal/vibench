# object_metadata.py
# [SAME-SCENARIO] Reads object metadata/HEAD information from Managed Object Storage (Amazon S3 example)

import os
import boto3
from botocore.exceptions import ClientError
from storage_client import create_s3_client
from storage_models import MetadataResult


def get_metadata(bucket: str, key: str) -> MetadataResult:
    """Retrieves metadata/HEAD for an object and returns normalized result.
    Args:
        bucket (str): Bucket name.
        key (str): Object key/path.
    Returns:
        MetadataResult: Size, content type, and metadata dict.
    Raises:
        FileNotFoundError: If object does not exist.
    """
    s3 = create_s3_client()
    try:
        head = s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        # 404 when object not found, re-raise as FileNotFoundError for clarity
        raise FileNotFoundError(f"Object {key} not found in bucket {bucket}.") from e
    # Normalize response
    return MetadataResult(
        size=head.get("ContentLength", 0),
        content_type=head.get("ContentType", "") or head.get("Content-Type", ""),
        metadata=head.get("Metadata", {}),
    )


# Example usage (uncomment to test)
# try:
#     meta = get_metadata('my-bucket', 'example.txt')
#     print(meta)
# except FileNotFoundError as fnf:
#     print(fnf)
