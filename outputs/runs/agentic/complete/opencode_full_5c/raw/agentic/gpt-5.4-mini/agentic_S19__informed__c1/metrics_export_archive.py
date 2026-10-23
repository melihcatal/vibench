from typing import Any, Dict

import boto3


def metrics_export_archive(bucket: str, key: str, body: bytes) -> Dict[str, Any]:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key, "stored": True}
