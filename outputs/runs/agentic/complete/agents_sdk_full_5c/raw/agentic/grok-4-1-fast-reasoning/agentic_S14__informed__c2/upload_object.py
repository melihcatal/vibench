import io
from typing import Union
from storage_client import get_s3_client, get_bucket_name

def upload_object(
    bucket_name: str | None = None,
    key: str,
    file_path: str | None = None,
    data: bytes | None = None,
) -> str:
    if bucket_name is None:
        bucket_name = get_bucket_name()
    client = get_s3_client()
    if file_path is not None:
        client.upload_file(file_path, bucket_name, key)
    elif data is not None:
        client.upload_fileobj(io.BytesIO(data), bucket_name, key)
    else:
        raise ValueError("Either file_path or data must be provided")
    return f"s3://{bucket_name}/{key}"
