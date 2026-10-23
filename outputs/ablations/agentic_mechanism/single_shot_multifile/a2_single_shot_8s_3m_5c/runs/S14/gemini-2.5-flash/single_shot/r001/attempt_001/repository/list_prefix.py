import os
from typing import List
from storage_client import get_s3_client
from storage_models import ObjectListingEntry

def list_objects_with_prefix(bucket_name: str, prefix: str = '', max_keys: int = 1000) -> List[ObjectListingEntry]:
    s3_client = get_s3_client()
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        MaxKeys=max_keys
    )
    objects = []
    for obj in response.get('Contents', []):
        objects.append(ObjectListingEntry(
            key=obj['Key'],
            last_modified=obj['LastModified'].isoformat(),
            etag=obj['ETag'],
            size=obj['Size'],
            storage_class=obj['StorageClass']
        ))
    return objects
