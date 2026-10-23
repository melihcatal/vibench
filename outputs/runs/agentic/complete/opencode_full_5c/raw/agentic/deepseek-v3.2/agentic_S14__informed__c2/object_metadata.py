import boto3
import os
from botocore.exceptions import ClientError
from storage_client import get_s3_client


def get_object_metadata(bucket_name, object_key):
    """
    Read object metadata or head information from Amazon S3.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key

    Returns:
        dict: Object metadata or error
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        metadata = {
            "success": True,
            "bucket": bucket_name,
            "key": object_key,
            "content_length": response.get("ContentLength"),
            "content_type": response.get("ContentType"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag"),
            "storage_class": response.get("StorageClass"),
            "provider": "Amazon S3",
        }

        # Add user metadata if present
        if "Metadata" in response:
            metadata["user_metadata"] = response["Metadata"]

        # Add server-side encryption info if present
        if "ServerSideEncryption" in response:
            metadata["server_side_encryption"] = response["ServerSideEncryption"]

        return metadata

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == "404":
            return {
                "success": False,
                "error": "Object not found",
                "provider": "Amazon S3",
            }
        else:
            return {"success": False, "error": str(e), "provider": "Amazon S3"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon S3"}
