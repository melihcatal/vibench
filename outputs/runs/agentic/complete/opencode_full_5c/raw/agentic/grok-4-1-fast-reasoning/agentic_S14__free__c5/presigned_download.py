from typing import Optional
from storage_client import create_aws_client


def create_presigned_download_url(bucket: str, key: str, expiration: int = 3600) -> str:
    client = create_aws_client("s3")
    url = client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expiration
    )
    return url
