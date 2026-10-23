import json
import os
from typing import Any, Dict

import boto3


def image_asset_archive(bucket: str, key: str, artifact: Dict[str, Any]) -> str:
    client = boto3.client(
        "s3", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    )
    body = json.dumps(artifact).encode("utf-8")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return f"s3://{bucket}/{key}"
