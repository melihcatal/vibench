from storage_client import get_storage_client
from storage_models import ObjectInfo
from typing import List
from botocore.exceptions import ClientError

def list_objects_prefix(bucket: str, prefix: str = '') -&gt; List[ObjectInfo]:
    """
    List Amazon S3 objects under a bucket prefix.
    """
    client = get_storage_client()
    try:
        paginator = client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        objects: List[ObjectInfo] = []
        for page in pages.search('Contents'):
            for obj in page:
                objects.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'etag': obj.get('ETag')
                })
        return objects
    except ClientError as e:
        raise ValueError(f"S3 list_objects_v2 failed: {e}")