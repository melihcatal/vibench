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
        # Get object metadata from S3
        response = s3_client.head_object(Bucket=request.bucket, Key=request.key)

        # Extract metadata
        metadata = {
            "content_type": response.get("ContentType"),
            "content_length": response.get("ContentLength"),
            "last_modified": response.get("LastModified"),
            "etag": response.get("ETag"),
            "storage_class": response.get("StorageClass"),
        }

        # Add custom metadata if present
        if "Metadata" in response:
            metadata["user_metadata"] = response["Metadata"]

        return MetadataResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            metadata=metadata,
            message=f"Retrieved metadata for s3://{request.bucket}/{request.key}",
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return MetadataResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error_message=f"Object not found in S3: s3://{request.bucket}/{request.key}",
            )
        else:
            return MetadataResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error_message=f"S3 metadata error: {str(e)}",
            )
    except Exception as e:
        return MetadataResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Metadata retrieval error: {str(e)}",
        )
