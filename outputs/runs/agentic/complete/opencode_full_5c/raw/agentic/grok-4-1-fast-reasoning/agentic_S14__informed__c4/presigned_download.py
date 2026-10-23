import boto3
from typing import Dict, Any
from storage_client import get_aws_client_kwargs


def presigned_download(bucket: str, key: str, expiration: int = 3600) -> str:
    kwargs = get_aws_client_kwargs()
    s3_client = boto3.client("s3", **kwargs)
    url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expiration
    )
    return url
