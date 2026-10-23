import os
import uuid

import boto3


def record_export_archive(bucket, record, key=None):
    s3 = boto3.client("s3")
    object_key = key or f"archives/{uuid.uuid4().hex}.json"
    s3.put_object(
        Bucket=bucket,
        Key=object_key,
        Body=record
        if isinstance(record, (bytes, bytearray))
        else str(record).encode("utf-8"),
        ContentType="application/json",
    )
    return {"bucket": bucket, "key": object_key}
