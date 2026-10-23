from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse

def get_object_metadata(
    request: ObjectMetadataRequest
) -> ObjectMetadataResponse:
    """
    Reads object metadata or head information from AWS S3 managed object storage.
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name,
            Key=request.object_key
        )
        # Clean up response to only include relevant metadata
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "LastModified": response.get("LastModified"),
            "ETag": response.get("ETag", "").strip('"'),
            "VersionId": response.get("VersionId"),
            "Metadata": response.get("Metadata", {})
        }
        return ObjectMetadataResponse(
            success=True,
            message="Object metadata retrieved successfully",
            metadata=metadata
        )
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return ObjectMetadataResponse(success=False, message="Object not found")
        return ObjectMetadataResponse(success=False, message=f"Error retrieving object metadata: {str(e)}")
    except Exception as e:
        return ObjectMetadataResponse(success=False, message=f"An unexpected error occurred: {str(e)}")
