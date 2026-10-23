from storage_client import StorageClient
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse
from botocore.exceptions import ClientError


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = StorageClient().get_s3_client()
    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name, Key=request.object_key
        )
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "LastModified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
            "ETag": response.get("ETag", "").strip('"'),
            "VersionId": response.get("VersionId"),
            "Metadata": response.get("Metadata", {}),
        }
        return ObjectMetadataResponse(
            success=True,
            metadata=metadata,
            message="Object metadata retrieved successfully.",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return ObjectMetadataResponse(
                success=False, message=f"Object not found: {request.object_key}"
            )
        return ObjectMetadataResponse(
            success=False, message=f"Error retrieving object metadata: {e}"
        )
