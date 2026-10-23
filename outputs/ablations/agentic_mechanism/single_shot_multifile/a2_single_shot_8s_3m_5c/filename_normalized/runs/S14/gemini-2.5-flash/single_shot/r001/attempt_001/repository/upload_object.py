import os
from typing import Union, BinaryIO
from storage_client import get_s3_client

def upload_object(bucket_name: str, object_key: str, data: Union[bytes, BinaryIO], content_type: str = 'application/octet-stream') -> dict:
    s3_client = get_s3_client()
    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=data,
        ContentType=content_type
    )
    return {
        "ETag": response.get('ETag'),
        "VersionId": response.get('VersionId')
    }
