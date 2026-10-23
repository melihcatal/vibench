import os
import json

import boto3


def record_export_archive(snapshot, bucket=None, key=None):
    s3 = boto3.client("s3")
    bucket_name = bucket or os.getenv("AWS_S3_BUCKET", "document-exports")
    object_key = key or "exports/snapshot.json"
    body = json.dumps(snapshot).encode("utf-8")
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)
    return {"bucket": bucket_name, "key": object_key, "ok": True}
