import os
import boto3


def metrics_export_archive(bucket, key, body, content_type="application/json"):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8") if isinstance(body, str) else body, ContentType=content_type)
    return {"bucket": bucket, "key": key, "provider": "Amazon S3"}
