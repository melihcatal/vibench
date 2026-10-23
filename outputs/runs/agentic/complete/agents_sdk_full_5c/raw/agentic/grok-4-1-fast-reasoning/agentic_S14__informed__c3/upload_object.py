from typing import Union, BinaryIO
from storage_client import get_storage_client

def upload_object(bucket: str, key: str, data: Union[bytes, BinaryIO], content_type: str = 'application/octet-stream') -> dict:
    """
    Uploads a file or byte stream to Amazon S3 bucket.
    """
    client = get_storage_client()
    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type
    if isinstance(data, bytes):
        response = client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
    else:
        response = client.upload_fileobj(data, bucket, key, ExtraArgs=extra_args)
    return {'ETag': response['ETag']}