import os
from storage_client import get_s3_client
from storage_models import ListedObject
from typing import List

def list_objects_with_prefix(bucket_name: str, prefix: str = '') -> List[ListedObject]:
    s3_client = get_s3_client()
    listed_objects: List[ListedObject] = []
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    listed_objects.append(ListedObject(
                        key=obj.get('Key', ''),
                        size=obj.get('Size', 0),
                        last_modified=obj.get('LastModified', '').isoformat()
                    ))
        print(f"Objects listed under prefix '''{prefix}''' in bucket '''{bucket_name}''' successfully.")
        return listed_objects
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []
