import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import MetadataRequest, MetadataResponse


def get_object_metadata(request: MetadataRequest) -> MetadataResponse:
    """Read object metadata or head information from AWS S3 managed object storage."""
    s3_client = get_s3_client()

    try:
        # Use head_object to get metadata without downloading the object
        response = s3_client.head_object(Bucket=request.bucket, Key=request.object_key)

        metadata = {
            "content_type": response.get("ContentType"),
            "content_length": response.get("ContentLength"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag"),
            "storage_class": response.get("StorageClass"),
            "server_side_encryption": response.get("ServerSideEncryption"),
            "metadata": response.get("Metadata", {}),
        }

        return MetadataResponse(
            success=True,
            metadata=metadata,
            bucket=request.bucket,
            object_key=request.object_key,
            message="Object metadata retrieved successfully",
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return MetadataResponse(
                success=False,
                error_message=f"Object not found in AWS S3: {request.bucket}/{request.object_key}",
            )
        return MetadataResponse(success=False, error_message=f"AWS S3 error: {str(e)}")
    except Exception as e:
        return MetadataResponse(
            success=False, error_message=f"Failed to retrieve metadata: {str(e)}"
        )
