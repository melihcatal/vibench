from typing import Any, Dict

import boto3


def record_export_archive(bucket: str, key: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.put_object(Bucket=bucket, Key=key, Body=str(payload).encode("utf-8"), ContentType="application/json")
    return {"bucket": bucket, "key": key, "archived": True}
