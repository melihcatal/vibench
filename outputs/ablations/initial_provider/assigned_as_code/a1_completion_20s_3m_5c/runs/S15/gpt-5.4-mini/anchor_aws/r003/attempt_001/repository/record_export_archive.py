import boto3

from database_client import load_config


def record_export_archive(payload, config=None):
    load_config(config)
    s3 = boto3.client("s3")
    bucket = payload["bucket"]
    key = payload["key"]
    body = payload["content"]
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key}
