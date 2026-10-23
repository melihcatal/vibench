import boto3

from database_client import load_config


def record_export_archive(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("s3", region_name=cfg["region"])
    bucket = cfg["object_bucket"]
    key = payload["key"]
    body = payload["content"]
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key}
