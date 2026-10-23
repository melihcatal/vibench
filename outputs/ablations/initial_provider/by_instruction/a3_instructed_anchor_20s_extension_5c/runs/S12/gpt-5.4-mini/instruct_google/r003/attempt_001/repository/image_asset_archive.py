from typing import Dict

import boto3


def image_asset_archive(bucket: str, key: str, body: bytes, metadata: Dict[str, str] | None = None) -> str:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=body, Metadata=metadata or {})
    return f"s3://{bucket}/{key}"
