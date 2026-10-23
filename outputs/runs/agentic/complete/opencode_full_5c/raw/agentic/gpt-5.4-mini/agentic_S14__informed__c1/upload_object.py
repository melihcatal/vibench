import base64
from typing import Union

from storage_client import load_storage_config, s3_client


def upload_object(
    bucket: str, key: str, body: Union[bytes, bytearray, str], content_type: str = None
):
    config = load_storage_config(bucket)
    client = s3_client()
    payload = body.encode("utf-8") if isinstance(body, str) else bytes(body)
    kwargs = {"Bucket": config.bucket, "Key": key, "Body": payload}
    if content_type:
        kwargs["ContentType"] = content_type
    return client.put_object(**kwargs)
