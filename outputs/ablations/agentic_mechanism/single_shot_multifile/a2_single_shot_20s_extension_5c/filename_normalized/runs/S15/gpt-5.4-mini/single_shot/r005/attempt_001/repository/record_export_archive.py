from typing import Any, Dict
import os
import boto3

s3 = boto3.client("s3")


def export_archive(payload: Dict[str, Any]) -> Dict[str, Any]:
    bucket = payload.get("bucket") or os.environ.get("ARCHIVE_BUCKET")
    if not bucket:
        raise RuntimeError("ARCHIVE_BUCKET is required")
    key = payload.get("key", "export/archive.json")
    body = payload.get("body", "")
    if isinstance(body, dict):
        import json
        body = json.dumps(body)
    s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8") if isinstance(body, str) else body)
    return {"ok": True, "bucket": bucket, "key": key}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return export_archive(event)
