import boto3
from storage_client import get_s3_client


def upload_object(
    bucket: str, key: str, data: bytes | str, content_type: str = None
) -> None:
    client = get_s3_client()
    if isinstance(data, str):
        data = data.encode("utf-8")
    extra_args = {"ContentType": content_type} if content_type else {}
    client.put_object(Bucket=bucket, Key=key, Body=data, **extra_args)
