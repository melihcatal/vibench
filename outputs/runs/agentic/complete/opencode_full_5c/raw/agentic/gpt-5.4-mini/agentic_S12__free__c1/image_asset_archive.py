import os
from typing import Dict

import boto3


s3 = boto3.client("s3")


def image_asset_archive(bucket: str, key: str, payload: Dict[str, str]) -> str:
    s3.put_object(Bucket=bucket, Key=key, Body=str(payload).encode("utf-8"))
    return f"s3://{bucket}/{key}"
