import io
import os
from pathlib import Path
from typing import BinaryIO, Union

import boto3


def upload_object(source: Union[str, bytes, bytearray, BinaryIO], bucket: str, key: str, region_name: str | None = None) -> str:
    session = boto3.session.Session(region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))
    s3 = session.client("s3")

    if isinstance(source, (bytes, bytearray)):
        body = io.BytesIO(source)
    elif isinstance(source, str):
        body = Path(source).open("rb")
    else:
        body = source

    try:
        s3.upload_fileobj(body, bucket, key)
    finally:
        if isinstance(source, str):
            body.close()

    return f"s3://{bucket}/{key}"
