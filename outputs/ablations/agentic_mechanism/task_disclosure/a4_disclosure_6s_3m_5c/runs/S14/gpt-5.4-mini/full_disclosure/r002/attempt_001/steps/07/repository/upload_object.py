import os
from typing import Optional, Union

import boto3


def upload_object(bucket: str, key: str, data: Union[str, bytes, bytearray, memoryview], content_type: Optional[str] = None, region_name: Optional[str] = None) -> dict:
    session = boto3.session.Session(region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client = session.client("s3")
    body = data
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, "rb") as f:
                body = f.read()
        else:
            body = data.encode("utf-8")
    elif isinstance(data, memoryview):
        body = data.tobytes()
    elif isinstance(data, bytearray):
        body = bytes(data)
    kwargs = {"Bucket": bucket, "Key": key, "Body": body}
    if content_type:
        kwargs["ContentType"] = content_type
    response = client.put_object(**kwargs)
    return {"etag": response.get("ETag"), "version_id": response.get("VersionId"), "bucket": bucket, "key": key}
