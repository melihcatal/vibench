import boto3


def metrics_export_archive(payload, config=None):
    s3 = boto3.client("s3", region_name=(config or {}).get("region"))
    bucket = payload["bucket"]
    key = payload["key"]
    body = payload["content"]
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    return {"bucket": bucket, "key": key, "archived": True}
