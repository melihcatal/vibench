import json
from datetime import datetime, timezone

from database_client import database_config, s3_client
from database_models import DocumentResponse, normalize_document


def archive_record(record, prefix="archives"):
    cfg = database_config()
    doc = normalize_document(record) or {}
    bucket = cfg["aws_s3_bucket"]
    key = f"{prefix}/{doc.get('document_id', 'record')}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    s3_client().put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(doc).encode("utf-8"),
        ContentType="application/json",
    )
    return DocumentResponse(ok=True, data={"bucket": bucket, "key": key}).__dict__


def handler(event, context=None):
    return archive_record(event.get("record", event), event.get("prefix", "archives"))
