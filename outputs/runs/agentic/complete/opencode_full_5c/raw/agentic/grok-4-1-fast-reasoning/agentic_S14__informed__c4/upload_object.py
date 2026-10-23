import boto3
from pathlib import Path
from typing import Union, BinaryIO, Dict, Optional
from storage_client import get_aws_client_kwargs
from storage_models import UploadResponse


def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, str, Path, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> UploadResponse:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)

    if isinstance(data, str):
        data = Path(data).read_bytes()
    elif isinstance(data, Path):
        data = data.read_bytes()
    elif hasattr(data, "read"):
        data_bytes = data.read()
        if hasattr(data, "seek"):
            data.seek(0)
        data = data_bytes

    extra_args: Dict[str, Any] = {}
    if content_type:
        extra_args["ContentType"] = content_type
    if metadata:
        extra_args["Metadata"] = metadata

    response = s3_client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)

    return {
        "etag": response["ETag"].strip('"'),
        "version_id": response.get("VersionId"),
    }
