from storage_client import get_storage_client
from storage_models import ObjectMetadata
from botocore.exceptions import ClientError


def get_object_metadata(bucket_name: str, object_name: str) -> ObjectMetadata:
    """
    Retrieves metadata from an object without returning the object itself.
    """
    s3_client = get_storage_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)

        metadata = ObjectMetadata(
            metadata=response.get("Metadata", {}),
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength"),
            e_tag=response.get("ETag"),
        )
        return metadata
    except ClientError as e:
        raise e
