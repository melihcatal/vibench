from typing import List
from botocore.exceptions import ClientError
from storage_client import get_storage_client, get_bucket_name

def list_objects_by_prefix(prefix: str, bucket_name: str = None) -> List[str]:
    """
    Lists object keys in an S3 bucket that match a given prefix.

    :param prefix: The prefix to filter object keys by.
    :param bucket_name: The S3 bucket. Defaults to env config.
    :return: A list of object keys matching the prefix.
    """
    s3_client = get_storage_client()
    target_bucket = bucket_name or get_bucket_name()
    
    object_keys = []
    paginator = s3_client.get_paginator("list_objects_v2")

    try:
        page_iterator = paginator.paginate(Bucket=target_bucket, Prefix=prefix)
        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    object_keys.append(obj["Key"])
    except ClientError as e:
        print(f"Error listing objects with prefix '{prefix}': {e}")
        raise
        
    return object_keys
