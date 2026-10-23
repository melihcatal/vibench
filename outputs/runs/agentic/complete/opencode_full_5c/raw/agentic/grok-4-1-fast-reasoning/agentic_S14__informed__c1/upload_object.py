from pathlib import Path
from typing import Union
from storage_client import s3_config
import boto3


def upload_object(
    bucket: str, key: str, data: Union[bytes, str, Path], content_type: str = None
) -> str:
    client = boto3.client("s3", **s3_config)
    if isinstance(data, (str, Path)):
        with open(str(data), "rb") as f:
            body = f.read()
    else:
        body = data
    resp = client.put_object(
        Bucket=bucket, Key=key, Body=body, ContentType=content_type
    )
    return resp["ETag"]
