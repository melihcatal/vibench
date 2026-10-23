import os
from storage_client import get_s3_client
from storage_models import ObjectInfo

def get_object_metadata(bucket_name: str, object_key: str) -> ObjectInfo:
    s3_client = get_s3_client()
    response = s3_client.head_object(
        Bucket=bucket_name,
        Key=object_key
    )
    return ObjectInfo(
        key=object_key,
        size=response['ContentLength'],
        last_modified=response['LastModified'].isoformat(),
        etag=response['ETag'],
        metadata=response.get('Metadata', {})
    )
