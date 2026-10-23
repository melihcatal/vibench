import os
from typing import Dict

import boto3


def metrics_export_archive(bucket: str, key: str, body: bytes, content_type: str = "application/json") -> Dict[str, str]:
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "key": key, "status": "archived"}
