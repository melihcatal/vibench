import os
from typing import Dict, Any

import boto3


def image_asset_archive(analysis: Dict[str, Any], bucket: str, key: str):
    s3 = boto3.client("s3")
    body = (str(analysis) + "\n").encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="text/plain")
    return {"bucket": bucket, "key": key, "provider": "aws_s3"}
