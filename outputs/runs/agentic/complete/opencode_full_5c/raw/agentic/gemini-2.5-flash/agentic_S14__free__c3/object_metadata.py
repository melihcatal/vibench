from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from botocore.exceptions import ClientError


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    try:
        # The AWS S3 client retrieves object metadata using head_object.
        # This is a lightweight operation to get metadata without downloading the object.
        response = s3_client.head_object(
            Bucket=request.bucket_name, Key=request.object_key
        )
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "LastModified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
            "ETag": response.get("ETag"),
            "VersionId": response.get("VersionId"),
            "Metadata": response.get("Metadata", {}),
        }
        return ObjectMetadataResponse(
            success=True,
            message="Object metadata retrieved successfully",
            metadata=metadata,
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "NotFound":
            return ObjectMetadataResponse(
                success=False, message=f"Object not found: {request.object_key}"
            )
        return ObjectMetadataResponse(success=False, message=f"AWS S3 ClientError: {e}")
    except Exception as e:
        return ObjectMetadataResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
