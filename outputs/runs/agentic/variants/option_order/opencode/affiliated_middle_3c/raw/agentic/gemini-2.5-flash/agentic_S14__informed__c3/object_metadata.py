from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name, Key=request.object_name
        )
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "LastModified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
            "ETag": response.get("ETag"),
            "Metadata": response.get("Metadata", {}),
        }
        return ObjectMetadataResponse(
            success=True,
            message="Object metadata retrieved successfully.",
            metadata=metadata,
        )
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return ObjectMetadataResponse(
                success=False,
                message=f"Object {request.object_name} not found in bucket {request.bucket_name}.",
            )
        return ObjectMetadataResponse(
            success=False, message=f"Error retrieving object metadata: {str(e)}"
        )
    except Exception as e:
        return ObjectMetadataResponse(
            success=False, message=f"An unexpected error occurred: {str(e)}"
        )
