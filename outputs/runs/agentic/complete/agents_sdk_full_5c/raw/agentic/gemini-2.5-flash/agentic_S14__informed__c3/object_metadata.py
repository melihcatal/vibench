import os
from storage_client import get_s3_client
from storage_models import ObjectMetadata

def get_object_metadata(
    bucket_name: str,
    object_key: str
) -> ObjectMetadata:
    """
    Reads object metadata (head information) from an S3 object.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) of the object.

    Returns:
        An ObjectMetadata instance containing the object's metadata.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        return ObjectMetadata(
            key=object_key,
            size=response['ContentLength'],
            last_modified=response['LastModified'].isoformat(),
            e_tag=response['ETag'].strip('\"'), # Remove quotes from ETag
            content_type=response.get('ContentType'),
            metadata=response.get('Metadata')
        )
    except Exception as e:
        print(f"Error retrieving object metadata: {e}")
        raise
