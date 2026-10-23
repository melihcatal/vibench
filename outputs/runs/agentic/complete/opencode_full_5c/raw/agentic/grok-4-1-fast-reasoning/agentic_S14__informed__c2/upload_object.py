from typing import Union
import io
from storage_client import get_s3_client
from storage_models import UploadResponse

def upload_object(bucket: str, key: str, data: Union[bytes, str], content_type: str = 'application/octet-stream', metadata: dict = None) -&gt; str:
    client = get_s3_client()
    if isinstance(data, str):
        data = data.encode('utf-8')
    extra_args = {'ContentType': content_type}
    if metadata:
        extra_args['Metadata'] = metadata
    resp = client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
    return resp['ETag']