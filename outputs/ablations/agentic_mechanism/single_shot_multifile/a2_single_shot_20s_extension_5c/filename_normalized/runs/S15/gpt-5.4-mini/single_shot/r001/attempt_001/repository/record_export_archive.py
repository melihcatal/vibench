import base64
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import boto3

S3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))
BUCKET = os.getenv("EXPORT_ARCHIVE_BUCKET", "managed-document-export-archive")


def archive_export(payload: Dict[str, Any]) -> Dict[str, Any]:
    record = payload.get("record", payload)
    key = payload.get("archive_key") or f"exports/{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    body = json.dumps(record, ensure_ascii=False).encode("utf-8")
    if payload.get("attachment_b64"):
        attachment = base64.b64decode(payload["attachment_b64"])
        body += b"\n" + attachment
    S3.put_object(Bucket=BUCKET, Key=key, Body=body, ContentType="application/json")
    return {"bucket": BUCKET, "key": key, "archived": True}


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if not sys.stdin.isatty() else os.environ.get("DOCUMENT_JSON", "{}")
    print(json.dumps(archive_export(json.loads(raw or "{}"))))