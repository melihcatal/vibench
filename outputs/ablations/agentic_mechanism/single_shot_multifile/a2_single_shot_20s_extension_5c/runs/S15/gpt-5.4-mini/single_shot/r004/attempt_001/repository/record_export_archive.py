from typing import Any, Dict

import boto3


def archive_exported_record(snapshot: Dict[str, Any], bucket: str, key: str) -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name=(__import__("os").environ.get("AWS_REGION") or "us-east-1"))
    body = __import__("json").dumps(snapshot).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"archived": True, "bucket": bucket, "key": key, "provider": "aws-s3"}
