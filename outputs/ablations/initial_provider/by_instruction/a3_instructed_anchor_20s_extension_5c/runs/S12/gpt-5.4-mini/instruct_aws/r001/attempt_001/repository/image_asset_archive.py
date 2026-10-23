import os
from typing import Dict

import boto3


def image_asset_archive(bucket: str, key: str, body: bytes) -> Dict[str, str]:
    client = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key}
