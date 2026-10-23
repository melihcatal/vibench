import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from storage_client import get_s3_client
from storage_models import MetadataRequest, MetadataResponse


def get_object_metadata(request: MetadataRequest) -> MetadataResponse:
    """Read object metadata or head information from AWS S3."""
    s3_client = get_s3_client()

    try:
        # Head object to get metadata without downloading content
        response = s3_client.head_object(Bucket=request.bucket, Key=request.object_key)

        # Extract metadata
        metadata = {
            "content_length": response.get("ContentLength", 0),
            "content_type": response.get("ContentType", "application/octet-stream"),
            "last_modified": response.get("LastModified", datetime.now()),
            "etag": response.get("ETag", "").strip('"'),
            "storage_class": response.get("StorageClass", "STANDARD"),
        }

        # Add user metadata if present
        if "Metadata" in response:
            metadata["user_metadata"] = response["Metadata"]

        # Add other headers
        for key, value in response.items():
            if key not in ["ResponseMetadata", "Metadata"] and key not in metadata:
                metadata[key.lower()] = value

        return MetadataResponse(
            success=True,
            object_key=request.object_key,
            bucket=request.bucket,
            metadata=metadata,
            message=f"Retrieved metadata from AWS S3 for s3://{request.bucket}/{request.object_key}",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"] if "Error" in e.response else "Unknown"
        if error_code == "404":
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
            message=f"Failed to retrieve metadata from AWS S3: {error_code}",
        )
    except Exception as e:
        return MetadataResponse(
            success=False,
            object_key=request.object_key,
            bucket=request.bucket,
            error_message=str(e),
            message=f"Failed to retrieve metadata: {str(e)}",
        )
