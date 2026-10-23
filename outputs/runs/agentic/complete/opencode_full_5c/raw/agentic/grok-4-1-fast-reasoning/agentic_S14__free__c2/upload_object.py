from pathlib import Path
from typing import Union, Dict, Any
from storage_client import get_s3_client


def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, Path, str],
    content_type: str = "application/octet-stream",
) -> Dict[str, Any]:
    client = get_s3_client()
    if isinstance(data, (str, Path)):
        data = Path(data).read_bytes()
    response = client.put_object(
        Bucket=bucket, Key=key, Body=data, ContentType=content_type
    )
    return {"bucket": bucket, "key": key, "etag": response["ETag"]}
