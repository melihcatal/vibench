import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ObjectMetadata


def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata:
    """
    Read object metadata (head information) from Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in S3

    Returns:
        ObjectMetadata object with metadata information
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        metadata = ObjectMetadata(
            bucket=bucket_name,
            key=object_key,
            size=response.get("ContentLength", 0),
            content_type=response.get("ContentType", ""),
            last_modified=response.get("LastModified"),
            etag=response.get("ETag", "").strip('"'),
            storage_class=response.get("StorageClass", "STANDARD"),
            metadata=response.get("Metadata", {}),
            version_id=response.get("VersionId"),
        )

        return metadata
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise Exception(f"Object not found: {bucket_name}/{object_key}")
        raise Exception(f"Failed to get object metadata: {e}")
