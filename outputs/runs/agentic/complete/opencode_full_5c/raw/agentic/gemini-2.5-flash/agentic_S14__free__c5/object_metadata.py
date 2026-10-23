from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(
            Bucket=request.bucket_name, Key=request.object_key
        )
        # Extract relevant metadata
        metadata = {
            k.lower(): v
            for k, v in response.items()
            if k not in ["ResponseMetadata", "ETag", "LastModified"]
        }
        # Custom metadata might be in 'Metadata' dict
        if "Metadata" in response:
            metadata.update(response["Metadata"])

        return ObjectMetadataResponse(
            success=True,
            metadata=metadata,
            message=f"Metadata for {request.object_key} retrieved successfully.",
        )
    except s3_client.exceptions.NoSuchKey:
        return ObjectMetadataResponse(
            success=False,
            metadata=None,
            message=f"Object {request.object_key} not found in bucket {request.bucket_name}.",
        )
    except Exception as e:
        return ObjectMetadataResponse(
            success=False,
            metadata=None,
            message=f"Failed to retrieve metadata for {request.object_key}: {str(e)}",
        )
