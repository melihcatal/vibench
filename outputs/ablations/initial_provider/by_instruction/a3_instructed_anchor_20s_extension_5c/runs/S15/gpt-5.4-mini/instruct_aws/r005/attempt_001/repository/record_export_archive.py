import os

import boto3

from database_models import normalize_item


def record_export_archive(record, bucket=None, key=None):
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    item = normalize_item(record) or {}
    bucket = bucket or os.getenv("EXPORT_ARCHIVE_BUCKET")
    key = key or f"exports/{item.get('document_id', 'record')}.json"
    body = str(item).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json")
    return {"bucket": bucket, "key": key, "archived": True}
