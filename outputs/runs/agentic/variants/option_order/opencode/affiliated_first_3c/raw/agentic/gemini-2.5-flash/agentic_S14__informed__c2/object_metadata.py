from storage_client import get_s3_client
from storage_models import ObjectMetadataResponse


def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadataResponse:
    """
    Reads object metadata (head information) from Amazon S3.
    """
    s3_client = get_s3_client()
    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    return ObjectMetadataResponse(
        metadata=response.get("Metadata", {}),
        content_length=response.get("ContentLength", 0),
        last_modified=response.get("LastModified"),
    )
