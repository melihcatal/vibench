from pathlib import Path
from typing import Union, Optional
from storage_client import create_aws_client
from storage_models import ObjectMetadata


def upload_object(
    bucket: str, key: str, data: Union[bytes, Path], content_type: Optional[str] = None
) -> None:
    if not isinstance(data, bytes):
        data = Path(data).read_bytes()

    client = create_aws_client("s3")
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
