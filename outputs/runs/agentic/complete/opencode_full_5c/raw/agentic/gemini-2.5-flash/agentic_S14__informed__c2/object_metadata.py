from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse


def get_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=request.bucket_name, Key=request.key)
        # Extract relevant metadata, typically from the 'ResponseMetadata' and top-level keys
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "LastModified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
            "ETag": response.get("ETag", "").strip("\"'"),
            "VersionId": response.get("VersionId"),
            "StorageClass": response.get("StorageClass"),
            "Metadata": response.get("Metadata", {}),  # Custom metadata
        }

        return ObjectMetadataResponse(
            bucket_name=request.bucket_name, key=request.key, metadata=metadata
        )
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise FileNotFoundError(
                f"Object {request.key} not found in bucket {request.bucket_name}"
            )
        else:
            raise RuntimeError(
                f"Failed to get object metadata for {request.key} in {request.bucket_name}: {e}"
            )
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
