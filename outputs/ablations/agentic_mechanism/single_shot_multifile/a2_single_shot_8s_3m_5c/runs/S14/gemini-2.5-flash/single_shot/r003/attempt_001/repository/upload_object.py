import os
from typing import Union, BinaryIO
from storage_client import get_s3_client
from storage_models import UploadResult

def upload_object(bucket_name: str, object_key: str, data: Union[bytes, BinaryIO], content_type: str) -> UploadResult:
    s3_client = get_s3_client()
    
    if isinstance(data, bytes):
        body = data
    else:
        data.seek(0)
        body = data.read()

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
        ContentType=content_type
    )
    
    return UploadResult(
        etag=response.get('ETag', '').strip('"'),
        version_id=response.get('VersionId')
    )
