import os

import boto3


def archive_export(snapshot_bytes, bucket, key):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=snapshot_bytes)
    return {"bucket": bucket, "key": key, "ok": True}
