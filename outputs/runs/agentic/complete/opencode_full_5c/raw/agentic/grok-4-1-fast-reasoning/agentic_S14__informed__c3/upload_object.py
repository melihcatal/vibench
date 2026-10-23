from typing import Optional
from storage_client import get_s3_client, get_bucket


def upload_object(
    key: str, file_path: Optional[str] = None, data: Optional[bytes] = None
):
    if file_path is None and data is None:
        raise ValueError("Either file_path or data must be provided")
    client = get_s3_client()
    bucket = get_bucket()
    if file_path:
        client.upload_file(file_path, bucket, key)
    else:
        client.put_object(Bucket=bucket, Key=key, Body=data)
