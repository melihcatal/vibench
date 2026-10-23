import io
from pathlib import Path
from typing import Union
from storage_client import get_storage_client


def upload_object(
    bucket: str,
    object_key: str,
    data: Union[str, Path, bytes, io.IOBase],
    content_type: str | None = None,
) -> dict:
    client = get_storage_client()
    extra_args = {"ContentType": content_type} if content_type else {}
    if isinstance(data, (str, Path)):
        filename = str(data)
        client.upload_file(
            Filename=filename, Bucket=bucket, Key=object_key, ExtraArgs=extra_args
        )
    elif isinstance(data, bytes):
        bio = io.BytesIO(data)
        client.upload_fileobj(
            Fileobj=bio, Bucket=bucket, Key=object_key, ExtraArgs=extra_args
        )
    else:
        client.upload_fileobj(
            Fileobj=data, Bucket=bucket, Key=object_key, ExtraArgs=extra_args
        )
    return {"bucket": bucket, "object_key": object_key}
