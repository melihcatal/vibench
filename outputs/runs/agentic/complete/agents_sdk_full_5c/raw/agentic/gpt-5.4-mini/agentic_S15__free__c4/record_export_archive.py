from __future__ import annotations

from typing import Any, Dict, Mapping

import boto3

from database_models import normalize_document


def record_export_archive(record: Mapping[str, Any], bucket_name: str, object_key: str) -> Dict[str, Any]:
    s3 = boto3.client("s3", region_name="us-east-1")
    payload = normalize_document(dict(record))
    body = str(payload).encode("utf-8")
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=body, ContentType="application/json")
    return {"bucket": bucket_name, "key": object_key, "bytes": len(body)}
