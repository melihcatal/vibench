import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(
    request: ObjectMetadataRequest
) -> ObjectMetadataResponse:
    """
    Reads object metadata from AWS S3 managed object storage.
    """
    s3_client = get_storage_client()

    try:
        response = s3_client.head_object(
            Bucket=os.getenv("AWS_S3_BUCKET_NAME", "default-bucket"),
            Key=request.object_key
        )

        return ObjectMetadataResponse(
            object_key=request.object_key,
            metadata=response.get("Metadata", {}),
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength"),
            last_modified=response.get("LastModified"),
            etag=response.get("ETag"),
            success=True
        )
    except ClientError as e:
        return ObjectMetadataResponse(
            object_key=request.object_key,
            metadata={},
            content_type="",
            content_length=0,
            last_modified=None,
            etag="",
            success=False,
            error=str(e)
        )