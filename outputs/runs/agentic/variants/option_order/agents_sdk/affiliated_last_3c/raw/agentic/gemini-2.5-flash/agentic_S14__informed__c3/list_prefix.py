from typing import List
from storage_client import get_s3_client
from storage_models import StorageObject

def list_objects_with_prefix(bucket_name: str, prefix: str = "") -> List[StorageObject]:
    """
    Lists stored objects under a given bucket or container prefix in Amazon S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter objects by.

    Returns:
        List[StorageObject]: A list of StorageObject instances.
    """
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    objects = []
    if 'Contents' in response:
        for item in response['Contents']:
            objects.append(StorageObject(
                bucket_name=bucket_name,
                key=item.get('Key'),
                size=item.get('Size'),
                last_modified=item.get('LastModified').isoformat() if item.get('LastModified') else None
            ))
    return objects
