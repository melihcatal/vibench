import boto3
from pathlib import Path
from typing import Union, Optional
from storage_client import S3_CONFIG, BUCKET_NAME
from storage_models import ObjectMetadata

def upload_object(
    key: str,
    data: Union[str, bytes, Path],
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None
) -> str:
    if isinstance(data, str):
        body = data.encode('utf-8')
        if content_type is None:
            content_type = 'text/plain; charset=utf-8'
    elif isinstance(data, Path):
        body = data.read_bytes()
        if content_type is None:
            content_type = 'application/octet-stream'
    else:
        body = data
        if content_type is None:
            content_type = 'application/octet-stream'

    extra_args = {'ContentType': content_type}
    if metadata:
        extra_args['Metadata'] = metadata

    client = boto3.client('s3', **S3_CONFIG)
    resp = client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=body,
        **extra_args
    )
    return resp['ETag']
