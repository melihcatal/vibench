import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import MetadataRequest, MetadataResponse


def get_object_metadata(request: MetadataRequest) -> MetadataResponse:
    """
    Reads object metadata or head information from AWS S3 managed object storage.
    """
    s3_client = get_s3_client()

    try:
        # Head object to get metadata without downloading content
        response = s3_client.head_object(Bucket=request.bucket, Key=request.object_key)

        metadata = {
            "content_length": response.get("ContentLength"),
            "content_type": response.get("ContentType"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag"),
            "storage_class": response.get("StorageClass"),
            "server_side_encryption": response.get("ServerSideEncryption"),
            "metadata": response.get("Metadata", {}),
        }

        return MetadataResponse(
            success=True,
            object_key=request.object_key,
            bucket=request.bucket,
            metadata=metadata,
            message=f"Retrieved metadata for s3://{request.bucket}/{request.object_key}",
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return MetadataResponse(
                success=False,
                object_key=request.object_key,
                bucket=request.bucket,
                error_message="Object not found",
                message=f"Object s3://{request.bucket}/{request.object_key} not found in AWS S3",
            )
        return MetadataResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to retrieve metadata from AWS S3: {e}",
        )
