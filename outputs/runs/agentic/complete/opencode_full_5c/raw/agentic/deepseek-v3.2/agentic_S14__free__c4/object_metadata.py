import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
import datetime


def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResponse:
    """
    Reads object metadata or head information from AWS S3 managed object storage.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket

    Returns:
        ObjectMetadataResponse with object metadata details
    """
    s3_client = get_s3_client()

    try:
        # Use head_object to get metadata without downloading the object
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        # Extract metadata
        metadata = {
            "ContentLength": response.get("ContentLength", 0),
            "ContentType": response.get("ContentType", "application/octet-stream"),
            "ETag": response.get("ETag", ""),
            "LastModified": response.get("LastModified", datetime.datetime.now()),
            "StorageClass": response.get("StorageClass", "STANDARD"),
        }

        # Extract user metadata
        user_metadata = response.get("Metadata", {})

        # Extract server-side encryption info if present
        encryption = response.get("ServerSideEncryption")
        kms_key_id = response.get("SSEKMSKeyId")

        return ObjectMetadataResponse(
            success=True,
            bucket=bucket_name,
            key=object_key,
            size=metadata["ContentLength"],
            content_type=metadata["ContentType"],
            etag=metadata["ETag"],
            last_modified=metadata["LastModified"].isoformat()
            if hasattr(metadata["LastModified"], "isoformat")
            else str(metadata["LastModified"]),
            storage_class=metadata["StorageClass"],
            metadata=user_metadata,
            server_side_encryption=encryption,
            kms_key_id=kms_key_id,
            provider="aws_s3",
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        if error_code == "404":
            return ObjectMetadataResponse(
                success=False,
                error_message=f"Object not found: {bucket_name}/{object_key}",
                error_code="NOT_FOUND",
                provider="aws_s3",
            )
        else:
            return ObjectMetadataResponse(
                success=False,
                error_message=str(e),
                error_code=error_code,
                provider="aws_s3",
            )
    except Exception as e:
        return ObjectMetadataResponse(
            success=False, error_message=str(e), provider="aws_s3"
        )


def object_exists(bucket_name: str, object_key: str) -> bool:
    """
    Check if an object exists in S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket

    Returns:
        True if object exists, False otherwise
    """
    try:
        s3_client = get_s3_client()
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise


if __name__ == "__main__":
    # Example usage
    request = ObjectMetadataRequest(bucket="my-example-bucket", key="test/example.txt")
    result = get_object_metadata(request.bucket, request.key)
    print(f"Metadata result: {result.success}")
    if result.success:
        print(f"Object size: {result.size} bytes")
        print(f"Content type: {result.content_type}")
        print(f"Last modified: {result.last_modified}")
        print(f"Storage class: {result.storage_class}")
