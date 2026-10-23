from typing import Union
from pathlib import Path
from storage_client import get_s3_client


def upload_object(bucket: str, key: str, content: Union[bytes, Path]) -> None:
    client = get_s3_client()
    if isinstance(content, Path):
        client.upload_file(Filename=str(content), Bucket=bucket, Key=key)
    else:
        client.put_object(Bucket=bucket, Key=key, Body=content)
