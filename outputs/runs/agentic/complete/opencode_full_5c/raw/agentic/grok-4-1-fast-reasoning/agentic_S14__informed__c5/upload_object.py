from typing import Union
from pathlib import Path
from storage_client import get_s3_client


def upload_object(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, Path, str],
    content_type: str = None,
) -> dict:
    if isinstance(data, str):
        data = Path(data)
    if isinstance(data, Path):
        data = data.read_bytes()
    client = get_s3_client()
    if content_type is None:
        content_type = "application/octet-stream"
    client.put_object(
        Bucket=bucket_name, Key=object_name, Body=data, ContentType=content_type
    )
    return {"bucket": bucket_name, "key": object_name}
