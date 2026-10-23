import os

import boto3


def record_export_archive(bucket, key, body):
    client = boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1",
    )
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body
        if isinstance(body, (bytes, bytearray))
        else str(body).encode("utf-8"),
    )
    return {"bucket": bucket, "key": key, "ok": True}
