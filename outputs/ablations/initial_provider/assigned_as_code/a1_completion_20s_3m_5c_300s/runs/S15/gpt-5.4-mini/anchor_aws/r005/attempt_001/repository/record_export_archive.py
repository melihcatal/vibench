import boto3

from database_client import get_s3_client


def record_export_archive(payload, config=None):
    client, bucket_name = get_s3_client(config)
    key = payload["key"]
    body = payload.get("body", b"")
    client.put_object(Bucket=bucket_name, Key=key, Body=body)
    return {"bucket": bucket_name, "key": key}
