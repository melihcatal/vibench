from typing import Dict, Any
from storage_client import get_s3_client
from storage_models import ObjectMetadata

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectMetadata:
    """
    Reads object metadata (Head Object) from Amazon S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key (path) of the object in the bucket.

    Returns:
        ObjectMetadata: An object containing the object's metadata.
    """
    s3_client = get_s3_client()
    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

    return ObjectMetadata(
        etag=response.get('ETag', '').strip(''"'),
        content_type=response.get('ContentType', 'application/octet-stream'),
        content_length=response.get('ContentLength', 0),
        last_modified=response.get('LastModified').isoformat() if response.get('LastModified') else '',
        custom_metadata=response.get('Metadata')
    )
