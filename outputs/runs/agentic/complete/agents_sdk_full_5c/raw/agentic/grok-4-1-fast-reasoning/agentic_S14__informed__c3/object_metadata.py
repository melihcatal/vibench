from storage_client import get_storage_client
from storage_models import ObjectMetadata
from botocore.exceptions import ClientError

def get_object_metadata(bucket: str, key: str) -> ObjectMetadata:
    """
    Retrieves metadata for an object in Amazon S3.
    """
    client = get_storage_client()
    try:
        response = client.head_object(Bucket=bucket, Key=key)
        return ObjectMetadata(
            key=key,
            e_tag=response['ETag'],
            size=response['ContentLength'],
            last_modified=response['LastModified'],
            content_type=response.get('ContentType'),
            metadata={k: v for k, v in response.get('Metadata', {}).items()}
        )
    except ClientError as e:
        raise ValueError(f"Object not found or error: {e}")