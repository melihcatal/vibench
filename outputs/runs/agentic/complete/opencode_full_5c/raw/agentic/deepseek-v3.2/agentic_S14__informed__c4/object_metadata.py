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
        object_key: Object key (path) in the bucket

    Returns:
        ObjectMetadata object with metadata fields
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        metadata = ObjectMetadata(
            key=object_key,
            bucket=bucket_name,
            size=response.get("ContentLength", 0),
            content_type=response.get("ContentType", ""),
            etag=response.get("ETag", "").strip('"'),
            last_modified=response.get("LastModified"),
            version_id=response.get("VersionId"),
            storage_class=response.get("StorageClass", "STANDARD"),
            metadata=response.get("Metadata", {}),
        )

        # Add any additional headers as custom metadata
        for key, value in response.items():
            if key not in [
                "ResponseMetadata",
                "ContentLength",
                "ContentType",
                "ETag",
                "LastModified",
                "VersionId",
                "StorageClass",
                "Metadata",
            ]:
                metadata.custom_headers[key] = value

        return metadata

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            raise FileNotFoundError(
                f"Object {object_key} not found in bucket {bucket_name}"
            )
        elif error_code == "403":
            raise PermissionError(
                f"Access denied to object {object_key} in bucket {bucket_name}"
            )
        else:
            raise Exception(f"S3 error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def check_object_exists(bucket_name: str, object_key: str) -> bool:
    """
    Check if an object exists in S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket

    Returns:
        True if object exists, False otherwise
    """
    s3_client = get_s3_client()

    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise
    except Exception:
        return False
