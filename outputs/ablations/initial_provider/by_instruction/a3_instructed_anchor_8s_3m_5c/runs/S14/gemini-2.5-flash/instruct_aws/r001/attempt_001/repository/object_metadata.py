from datetime import datetime
from storage_client import StorageClient
from storage_models import ObjectMetadataResponse

def get_object_metadata(bucket_name: str, object_name: str) -> ObjectMetadataResponse:
    """Reads object metadata (head information) from AWS S3.

    Args:
        bucket_name: The name of the S3 bucket.
        object_name: The name of the object.

    Returns:
        An ObjectMetadataResponse containing the object's metadata.
    """
    s3_client = StorageClient.get_client()

    response = s3_client.head_object(
        Bucket=bucket_name,
        Key=object_name
    )
    
    # AWS S3 returns 'LastModified' as a datetime object
    last_modified_dt = response.get('LastModified')
    # Ensure last_modified is in a consistent string format, e.g., ISO 8601
    last_modified_str = last_modified_dt.isoformat() if isinstance(last_modified_dt, datetime) else str(last_modified_dt)

    return ObjectMetadataResponse(
        content_type=response.get('ContentType'),
        content_length=response.get('ContentLength'),
        last_modified=last_modified_str,
        etag=response.get('ETag', '').strip('\"\'),
        metadata=response.get('Metadata', {})
    )
