from typing import Any, Dict

import boto3


s3 = boto3.client("s3")


def image_asset_archive(bucket: str, key: str, body: bytes, content_type: str = "application/json") -> Dict[str, Any]:
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
    return {"bucket": bucket, "key": key, "provider": "amazon-s3"}
